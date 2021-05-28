import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# @register_job(scheduler, "cron", hour = 17, minute = 25, id = "test")
@register_job(scheduler, "interval", seconds = 5, id = "test_scheduler", replace_existing = True)
def test():
    print(datetime.datetime.now())

def gen_outpatient_dutyroster():
    pass

register_events(scheduler)
scheduler.start()
print("Scheduler started!")
