from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from cron import hour_logger_api


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(hour_logger_api.jira_hour_sync_to_erp,
                      CronTrigger.from_crontab('0 21 * * *', timezone="Asia/Dhaka"))
    scheduler.start()
