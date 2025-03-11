from flask_apscheduler import APScheduler

from .jobs import health_job


def register_jobs(scheduler: APScheduler):
    scheduler.add_job(id='16f55c5d330d85d522ad16582d3a019e', func=health_job, trigger='interval', seconds=90, replace_existing=True)
