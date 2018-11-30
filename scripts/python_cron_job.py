from scripts import run_and_save
from pytz import utc
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import sys
from time import sleep
import datetime

jobstores = {
    'default': MemoryJobStore(),
}
executors = {
    'default': ProcessPoolExecutor(1),
}
job_defaults = {
    'coalesce': True,
    'max_instances': 3
}



if __name__ == '__main__':
    scheduler = BackgroundScheduler(jobstores=jobstores,
                                    executors=executors,
                                    job_defaults=job_defaults,
                                    timezone=utc)
    scheduler.start()
    end_date = datetime.datetime.utcnow() + datetime.timedelta(days=5)
    print("scheduling job to run daily until..", end_date)

    job = scheduler.add_job(run_and_save.exec,
                            trigger='cron',
                            hour='1',
                            end_date=end_date
                      )
    print(job)

    while True:
        sleep(1)
        sys.stdout.write('.');
        sys.stdout.flush()

