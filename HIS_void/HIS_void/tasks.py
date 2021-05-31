import calendar

from django.utils import timezone, dateparse
from django.db import transaction
from django.db.utils import OperationalError

from his.models import DutyRoster
from outpatient.models import RemainingRegistration

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job


# 应该在全局设置中储存
AM_DELETE_TIME = dateparse.parse_time("12:05:00")
PM_DELETE_TIME = dateparse.parse_time("00:05:00")
DAY_INSERT_TIME = dateparse.parse_time("00:00:01")

# 测试用
# AM_DELETE_TIME = dateparse.parse_time("03:05:00")
# PM_DELETE_TIME = dateparse.parse_time("06:05:00")
# DAY_INSERT_TIME = dateparse.parse_time("09:38:01")
#
# import logging
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


def gen_remaining_registration():
    """
    产生自今天开始，7天的剩余挂号信息
    """
    # 该设置应该移出函数，放在统一配置文件中
    MAX_DAYS = 7
    # 垃圾代码
    # 待修改
    staff_duty_rosters = DutyRoster.objects.filter(
        duty_area__isnull = True, 
        medical_staff__dept__usergroup__ug_id__range = [1,9]
    )
    today = timezone.localdate()
    # 遍历一周7天
    remaining_regs = []
    with transaction.atomic():
        for dd in range(MAX_DAYS):
            dt = today + timezone.timedelta(days = dd)
            # calendar 中以 0 代表周一，作为一周起点
            weekday = calendar.weekday(dt.year, dt.month, dt.day) + 1
            day_duty_staffs = map(
                lambda d: d.medical_staff,
                staff_duty_rosters.filter(working_day = weekday)
            )
            # 遍历当天门诊值班医生，创建对应的剩余挂号记录
            for ms in day_duty_staffs:
                # 是否为 UTC 时间都可以正常以 UTC 时间存储进数据库
                reg_datetime = {
                    "AM": dateparse.parse_datetime(dt.__str__() + " 08:00:00").astimezone(timezone.utc),
                    "PM": dateparse.parse_datetime(dt.__str__() + " 13:00:00").astimezone(timezone.utc),
                }
                reg_num = int(ms.title.titleregisternumber.register_number / 2)
                remaining_regs += [
                    RemainingRegistration(
                        medical_staff = ms,
                        register_date = reg_datetime["AM"],
                        remain_quantity = reg_num
                    ),
                    RemainingRegistration(
                        medical_staff = ms,
                        register_date = reg_datetime["PM"],
                        remain_quantity = reg_num
                    )
                ]
        # bulk 插入记录
        RemainingRegistration.objects.bulk_create(remaining_regs)

def insert_day_remaining_registration():
    """
    插入当天的剩余挂号信息
    """
    today = timezone.localdate()
    # calendar 中以 0 代表周一，作为一周起点
    weekday = calendar.weekday(today.year, today.month, today.day) + 1
    # 垃圾代码
    # 待修改
    day_duty_staffs = map(
        lambda d: d.medical_staff,
        DutyRoster.objects.filter(
            working_day = weekday,
            duty_area__isnull = True, 
            medical_staff__dept__usergroup__ug_id__range = [1,9]
        )
    )
    remaining_regs = []
    with transaction.atomic():
        for ms in day_duty_staffs:
            # 是否为 UTC 时间都可以正常以 UTC 时间存储进数据库
            reg_datetime = {
                "AM": dateparse.parse_datetime(today.__str__() + " 08:00:00").astimezone(timezone.utc),
                "PM": dateparse.parse_datetime(today.__str__() + " 13:00:00").astimezone(timezone.utc),
            }
            reg_num = int(ms.title.titleregisternumber.register_number / 2)
            remaining_regs += [
                RemainingRegistration(
                    medical_staff = ms,
                    register_date = reg_datetime["AM"],
                    remain_quantity = reg_num
                ),
                RemainingRegistration(
                    medical_staff = ms,
                    register_date = reg_datetime["PM"],
                    remain_quantity = reg_num
                )
            ]
        # bulk 插入记录
        RemainingRegistration.objects.bulk_create(remaining_regs)


@register_job(
    scheduler, "cron", 
    hour = DAY_INSERT_TIME.hour, minute = DAY_INSERT_TIME.minute, second = DAY_INSERT_TIME.second, 
    id = "insert_remaining_registration",
    replace_existing = True
)
def insert_remaining_registration():
    """
    若剩余挂号信息表没有记录，则产生7天的记录；若存在记录，则产生今天的剩余挂号信息。
    """
    # 使用socket绑定固定端口，以端口的唯一性保证定时任务执行的唯一性
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 47200))
    except socket.error:
        print("定时任务已经启动")

    if RemainingRegistration.objects.count() == 0:
        gen_remaining_registration()
    else:
        insert_day_remaining_registration()


@register_job(
    scheduler, "cron", 
    hour = AM_DELETE_TIME.hour, minute = AM_DELETE_TIME.minute, second = AM_DELETE_TIME.second, 
    id = "delete_am_regs",
    replace_existing = True
)
def delete_past_am_remaining_registration():
    """
    删除过去上午时段的剩余挂号记录
    """
    now = dateparse.parse_datetime(
        timezone.localdate().__str__() + " " + AM_DELETE_TIME.__str__()
    ).astimezone(timezone.utc)
    with transaction.atomic():
        RemainingRegistration.objects.filter(
            register_date__lt = now
        ).delete()


@register_job(
    scheduler, "cron", 
    hour = PM_DELETE_TIME.hour, minute = PM_DELETE_TIME.minute, second = PM_DELETE_TIME.second, 
    id = "delete_pm_regs",
    replace_existing = True
)
def delete_past_pm_remaining_registration():
    """
    删除过去下午时段的剩余挂号记录
    """
    now = dateparse.parse_datetime(
        timezone.localdate().__str__() + " " + PM_DELETE_TIME.__str__()
    ).astimezone(timezone.utc)
    with transaction.atomic():
        RemainingRegistration.objects.filter(
            register_date__lt = now
        ).delete()


# 当第一次进行 migrate 时，表不存在，抛出 django.db.utils.OperationalError
try:
    register_events(scheduler)
    scheduler.start()
    print("\033[1;33mScheduler started!\033[0m")
except OperationalError:
    pass
