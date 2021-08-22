import sqlite3
from base import application_context


class Room:
    """creates room object for Google Meet room"""

    def __init__(self, name, code, time, days):
        """
        :param name: string containing name of meet room
        :param code: string containing google meet room code in xxx-yyyy-zzz format
        :param time: string containing time in h:mm AP format
        :param days: string containing days of week
        """

        self.name = name
        self.code = code
        self.time = time
        self.days = days
        self.days_longstr = self.get_days_longstr(days)

    @staticmethod
    def get_days_longstr(days_string):
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
        days_list = days_string.split()
        for day in days_list:
            new_days_list.append(days_conversion[day])

        return ",".join(new_days_list)


class RoomDatabase:
    """database for saving, reading, updating, and deleting data for room objects"""

    # dir_path = os.path.dirname(os.path.abspath(__file__))
    # DB_LOCATION = os.path.join(dir_path, "../resources/base/rooms.db")
    DB_LOCATION = application_context.get_resource("rooms.db")

    def __init__(self):
        self.connection = sqlite3.connect(RoomDatabase.DB_LOCATION)
        self.cursor = self.connection.cursor()

        # if table doesn't exist, it's created
        if not self._table_exists():
            self._create_table()
            self._commit()

    def close(self):
        """closes connection"""
        self.connection.close()

    def save_room(self, room):
        """adds room object to database"""
        self.cursor.execute(f"INSERT INTO rooms VALUES('{room.name}', '{room.code}',"
                            f" '{room.time}', '{room.days}')")
        self._commit()

    def edit_room(self, old_room, new_room):
        """updates room information"""
        self.cursor.execute(f"""UPDATE rooms SET name='{new_room.name}', code='{new_room.code}', time='{new_room.time}', 
                days='{new_room.days}' WHERE name='{old_room.name}' AND code='{old_room.code}' AND
                time='{old_room.time}'AND days='{old_room.days}'
            """)
        self._commit()

    def delete_room(self, room):
        """removes room object from database"""
        self.cursor.execute(f"""DELETE from rooms WHERE name='{room.name}' AND code='{room.code}' AND
                time='{room.time}'AND days='{room.days}'
            """)
        self._commit()

    def get_all_rooms(self):
        """retrieves all room objects in database"""
        self.cursor.execute("SELECT rowid, * from rooms")
        room_rows = self.cursor.fetchall()

        rooms = []
        for room_row in room_rows:
            rooms.append(Room(room_row[1], room_row[2], room_row[3], room_row[4]))

        return rooms

    def _table_exists(self):
        """ check if rooms table exists """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rooms'")
        return len(self.cursor.fetchall())

    def _create_table(self):
        self.cursor.execute("""CREATE TABLE rooms(
            name text, 
            code text, 
            time text, 
            days text
            )""")
        self._commit()

    def _commit(self):
        """commits changes to database"""
        self.connection.commit()
