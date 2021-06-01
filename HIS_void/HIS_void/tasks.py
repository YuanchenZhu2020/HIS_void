import calendar
import socket

from django.utils import timezone, dateparse
from django.db import transaction
from django.db.utils import OperationalError

from his.models import DutyRoster
from outpatient.models import RemainingRegistration

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job


# 应该在全局设置中储存
AM_ZERO_TIME = dateparse.parse_time("12:05:00")
PAST_DELETE_TIME = dateparse.parse_time("00:05:00")
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


class MultiJobExecError(Exception):
    """
    多线程下，多任务同时执行的错误
    """
    def __str__(self) -> str:
        return "\033[1;31m重复启动定时任务!!!\033[m"


def ensure_uniqueness_in_multiprocess(port):
    """
    使用socket绑定固定端口，以端口的唯一性保证定时任务执行的唯一性
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 端口复用，即多个socket绑定到同一端口，这里不能使用
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", port))
    except socket.error:
        print("定时任务已经启动")
        raise MultiJobExecError()


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
    max_instances = 1,
    replace_existing = True
)
def insert_remaining_registration():
    """
    若剩余挂号信息表没有记录，则产生7天的记录；若存在记录，则产生今天的剩余挂号信息。
    """
    try:
        ensure_uniqueness_in_multiprocess(47200)
    except MultiJobExecError:
        pass
    else:
        if RemainingRegistration.objects.count() == 0:
            gen_remaining_registration()
        else:
            insert_day_remaining_registration()


@register_job(
    scheduler, "cron", 
    hour = AM_ZERO_TIME.hour, minute = AM_ZERO_TIME.minute, second = AM_ZERO_TIME.second, 
    id = "zero_past_am_regs",
    max_instances = 1,
    replace_existing = True
)
def zero_past_am_remaining_registration():
    """
    将上午时段的剩余挂号数置为0

    筛选条件：挂号时间小于当日12:00:00 am

    p.s. 这里应该记录下当日12:00:00之前的剩余挂号数，以便进行数据分析
    """
    try:
        ensure_uniqueness_in_multiprocess(47201)
    except MultiJobExecError:
        pass
    else:
        now = dateparse.parse_datetime(
            timezone.localdate().__str__() + " 12:00:00"
        ).astimezone(timezone.utc)
        with transaction.atomic():
            RemainingRegistration.objects.filter(
                register_date__lt = now
            ).update(remain_quantity = 0)


@register_job(
    scheduler, "cron", 
    hour = PAST_DELETE_TIME.hour, minute = PAST_DELETE_TIME.minute, second = PAST_DELETE_TIME.second, 
    id = "delete_past_regs",
    max_instances = 1,
    replace_existing = True
)
def delete_past_remaining_registration():
    """
    删除前一天的剩余挂号记录

    筛选条件：挂号时间小于当天零点
    """
    try:
        ensure_uniqueness_in_multiprocess(47202)
    except MultiJobExecError:
        pass
    else:
        now = dateparse.parse_datetime(
            timezone.localdate().__str__() + " 00:00:00"
        ).astimezone(timezone.utc)
        with transaction.atomic():
            RemainingRegistration.objects.filter(
                register_date__lt = now
            ).delete()


# 当第一次进行 migrate 时，表不存在，抛出 django.db.utils.OperationalError
try:
    scheduler.start()
    print("\033[1;33mScheduler started!\033[0m")
except OperationalError:
    pass
