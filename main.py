from apscheduler.triggers.cron import CronTrigger

from database import RoomDatabase
from schedule import open_meet_room, scheduler


class Room:
    """creates room object for Google Meet room"""

    def __init__(self, name, code, time, days_list):
        """
        :param name: string containing name of meet room
        :param code: string containing meet room code in xxx-yyyy-zzz format or meet room nickname
        :param time: string containing time in h:mm AP format
        :param days_list: list containing days of week
        """

        self.name = name
        self.code = code
        self.time = time
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


def main():
    import time

    scheduler.start(paused=True)
    print(scheduler.get_jobs())

    database = RoomDatabase()

    print("Scheduled Rooms:")
    print("\t" + "ID".ljust(3) + "Name".ljust(20) + "Code".ljust(15) + "Time".ljust(10) + "Days".ljust(15))

    for room in database.get_all_rooms():
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
        database.save_room(room)
        database.close()

        # creating job and adding to scheduler
        time_obj = time.strptime(time_scheduled, "%I:%M %p")
        days_of_week_str = Room.days_longstr(days)

        trigger = CronTrigger(day_of_week=days_of_week_str,hour=time_obj.tm_hour, minute=time_obj.tm_min)

        job_id = f"{name}_{code}_{time_scheduled}_{days}"
        job = scheduler.add_job(open_meet_room, args=[room.code], trigger=trigger, id=job_id)

    # TODO: add to scheduler
    elif action_input == "E":
        id = int(input("ID of room to edit: "))
        print(f"Editing Room {id}:")
        name = input("\tName: ").strip()
        code = input("\tCode: ").strip()
        time_scheduled = input("\tTime: ").strip()
        days = input("\tDays: ").strip()

        old_room = database.get_room(id)
        job_id = f"{old_room[1]}_{old_room[2]}_{old_room[3]}_{old_room[4]}"

        # editing room info in database
        room = Room(name, code, time_scheduled, Room.days_listfstr(days))
        database.edit_room(id, room)
        database.close()

        # deleting old job then adding edited job
        scheduler.remove_job(job_id=job_id)

        # creating edited job to scheduler
        time_obj = time.strptime(time_scheduled, "%I:%M %p")
        days_of_week_str = Room.days_longstr(days)

        trigger = CronTrigger(day_of_week=days_of_week_str, hour=time_obj.tm_hour, minute=time_obj.tm_min)

        job_id = f"{name}_{code}_{time_scheduled}_{days}"
        job = scheduler.add_job(open_meet_room, args=[room.code], trigger=trigger, id=job_id)

    elif action_input == "D":
        id = int(input("ID of room to delete: "))

        # Getting room info from database to create job_id
        room = database.get_room(id)
        job_id = f"{room[1]}_{room[2]}_{room[3]}_{room[4]}"

        database.delete_room(id)
        database.close()

        scheduler.remove_job(job_id=job_id)

    else:
        print("Wrong input.")


if __name__ == "__main__":
    main()
