from apscheduler.schedulers.background import BackgroundScheduler
import webbrowser
import time


def open_meet_room(code):
    webbrowser.open(f"https://www.meet.google.com/{code}")


scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', url='sqlite:///data/scheduler_jobs.db')

if __name__ == "__main__":

    scheduler.start()
    print(scheduler.get_jobs())

    while True:
        time.sleep(1)
