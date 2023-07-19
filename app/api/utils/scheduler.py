# app/api/utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from .cleanup import update_axe_score_table

def start_scheduled_jobs():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_axe_score_table, 'interval', seconds=60)
    scheduler.start()


