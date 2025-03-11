from datetime import datetime

from logger import Log

log = Log()


def health_job():
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    log.info(f"Running health cronjob at {now}")
