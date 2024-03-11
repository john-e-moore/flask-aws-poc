import os
from apscheduler.schedulers.background import BackgroundScheduler
from .s3_utils import download_csv_from_s3
from ..config import Config

def schedule_csv_download():
    local_download_path = Config.PROJECTIONS_DOWNLOAD_LOCAL_KEY
    bucket = os.getenv('FLASK_S3_BUCKET')
    key = os.getenv('FLASK_S3_KEY')
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=download_csv_from_s3,
        trigger="interval",
        minutes=30,
        args=[bucket, key, local_download_path],
        name='Update CSV from S3',
        replace_existing=True
    )
    scheduler.start()
