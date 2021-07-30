import sqlite3
import os


class RoomDatabase:
    """database for saving, reading, updating, and deleting data for room objects"""

    dir_path = os.path.dirname(os.path.abspath(__file__))
    DB_LOCATION = os.path.join(dir_path, "data\\rooms.db")

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
                            f" '{room.time}', '{' '.join(room.days_list)}')")
        self._commit()

    def edit_room(self, room_id, new_room):
        """updates room information"""
        self.cursor.execute(f"""UPDATE rooms SET name='{new_room.name}', code='{new_room.code}', time='{new_room.time}', 
                days='{' '.join(new_room.days_list)}' WHERE rowid='{room_id}'
            """)
        self._commit()

    def delete_room(self, rowid):
        """removes room object from database"""
        self.cursor.execute(f"DELETE from rooms WHERE rowid='{rowid}'")
        self._commit()

    def get_all_rooms(self):
        """retrieves all room objects in database"""
        self.cursor.execute("SELECT rowid, * from rooms")
        rooms = self.cursor.fetchall()

        return rooms

    def get_room(self, id):
        """retrieves a room object based on rowid"""
        self.cursor.execute(f"SELECT rowid, * from rooms WHERE rowid='{id}'")
        return self.cursor.fetchone()

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
