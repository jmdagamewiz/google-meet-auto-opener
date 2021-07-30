from apscheduler.triggers.cron import CronTrigger
import time
import wmi
import os
import sys
import subprocess

from database import RoomDatabase
from schedule import open_meet_room, scheduler


class Room:
    """creates room object for Google Meet room"""

    def __init__(self, name, code, time_scheduled, days_list):
        """
        :param name: string containing name of meet room
        :param code: string containing meet room code in xxx-yyyy-zzz format or meet room nickname
        :param time_scheduled: string containing time in h:mm AP format
        :param days_list: list containing days of week
        """

        self.name = name
        self.code = code
        self.time = time_scheduled
        self.days_list = days_list
        self.days_str = self.days_strflist(self.days_list)

    @staticmethod
    def days_strflist(days_list):
        return " ".join(days_list)

    @staticmethod
    def days_listfstr(days_string):
        return days_string.split()

    @staticmethod
    def days_longstr(days_string):
        days_conversion = {
            'M': 'mon',
            'T': 'tue',
            'W': 'wed',
            'Th': 'thu',
            'F': 'fri',
            'S': 'sat',
            'Su': 'sun',
        }
        new_days_list = []
        days_list = Room.days_listfstr(days_string)
        for day in days_list:
            new_days_list.append(days_conversion[day])

        return ",".join(new_days_list)


class Window:

    def __init__(self):

        self.scheduler = scheduler
        self.scheduler.start(paused=True)
        self.scheduler.print_jobs()

        self.database = RoomDatabase()

    def create_job_from_room(self, room):
        """creates job object for scheduler using room object"""

        time_obj = time.strptime(room.time, "%I:%M %p")
        days_of_week_str = Room.days_longstr(Room.days_strflist(room.days_list))

        trigger = CronTrigger(day_of_week=days_of_week_str, hour=time_obj.tm_hour, minute=time_obj.tm_min)

        job_id = f"{room.name}_{room.code}_{room.time}_{Room.days_strflist(room.days_list)}"
        job = self.scheduler.add_job(open_meet_room, args=[room.code],
                                     trigger=trigger, id=job_id,
                                     misfire_grace_time=10)

    @staticmethod
    def restart_scheduler():
        """stops and runs scheduler for new jobs to be added to it"""

        # stops background process of scheduler
        f = wmi.WMI()
        for process in f.Win32_Process():
            if process.name == "pythonw.exe":
                process.Terminate()
                break

        dir_path = os.path.dirname(os.path.abspath(__file__))
        schedule_path = os.path.join(dir_path, "schedule.py")

        # runs background process of scheduler
        subprocess.Popen([sys.executable.replace("python", "pythonw"),
                          schedule_path], )

    def run(self):
        print("\t" + "ID".ljust(3) + "Name".ljust(20) + "Code".ljust(15) + "Time".ljust(10) + "Days".ljust(15))

        for room in self.database.get_all_rooms():
            print("\t" + f"{room[0]}".ljust(3) + f"{room[1]}".ljust(20) + f"{room[2]}".ljust(15) +
                  f"{room[3]}".ljust(10) + f"{room[4]}".ljust(15))
        print()

        action_input = input("Add(A), Edit(E), Delete(D) room: ").strip()
        action_input = action_input.capitalize()

        if action_input == "A":

            # getting input from user
            print("Adding new Room:")
            name = input("\tName: ").strip()
            code = input("\tCode: ").strip()
            time_scheduled = input("\tTime: ").strip()
            days = input("\tDays: ").strip()

            # saving room to database
            room = Room(name, code, time_scheduled, Room.days_listfstr(days))
            self.database.save_room(room)
            self.database.close()

            self.create_job_from_room(room)
            self.restart_scheduler()

        elif action_input == "E":
            id = int(input("ID of room to edit: "))
            print(f"Editing Room {id}:")
            name = input("\tName: ").strip()
            code = input("\tCode: ").strip()
            time_scheduled = input("\tTime: ").strip()
            days = input("\tDays: ").strip()

            old_room_tuple = self.database.get_room(id)
            old_room = Room(old_room_tuple[1], old_room_tuple[2], old_room_tuple[3], old_room_tuple[4])

            # editing room info in database
            new_room = Room(name, code, time_scheduled, Room.days_listfstr(days))
            self.database.edit_room(id, new_room)
            self.database.close()

            # deleting old job then adding edited job
            job_id = f"{old_room.name}_{old_room.code}_{old_room.time}_{Room.days_strflist(old_room.days_list)}"
            scheduler.remove_job(job_id=job_id)

            self.create_job_from_room(new_room)
            self.restart_scheduler()

        elif action_input == "D":
            id = int(input("ID of room to delete: "))

            # Getting room info from database to create job_id
            room_tuple = self.database.get_room(id)
            room = Room(room_tuple[1], room_tuple[2], room_tuple[3], room_tuple[4])

            self.database.delete_room(id)
            self.database.close()

            # deleting job
            job_id = f"{room.name}_{room.code}_{room.time}_{Room.days_strflist(room.days_list)}"
            self.scheduler.remove_job(job_id=job_id)
            self.restart_scheduler()

        else:
            print("Wrong input.")


if __name__ == "__main__":
    window = Window()
    window.run()
