from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import webbrowser
from base import application_context


def open_meet_room(code):
    webbrowser.open(f"https://meet.google.com/{code}")


# gets path of DB Location based on user
DB_LOCATION = application_context.get_resource("scheduler_jobs.db")

scheduler = BackgroundScheduler()
scheduler.add_jobstore(SQLAlchemyJobStore(url=f'sqlite:///{DB_LOCATION}'))
