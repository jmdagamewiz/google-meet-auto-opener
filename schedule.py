from apscheduler.schedulers.background import BackgroundScheduler
import webbrowser
import time
import os


def open_meet_room(code):
    webbrowser.open(f"https://meet.google.com/{code}")


# gets path of DB Location based on user
dir_path = os.path.dirname(os.path.abspath(__file__))
DB_LOCATION = os.path.join(dir_path, "data\\scheduler_jobs.db")

scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', url=f'sqlite:///{DB_LOCATION}')

if __name__ == "__main__":
    scheduler.start()

    while True:
        time.sleep(1)
