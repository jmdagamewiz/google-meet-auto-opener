from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QLabel, QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QStyle, QTimeEdit, QButtonGroup, QScrollArea
from PyQt5.QtCore import QSize, Qt, QPoint, QTime
from PyQt5.QtGui import QCursor
import sys

import math
from database import RoomDatabase


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


class EditRoomFrame(QFrame):
    """
    clickable, editable frame that contains all information
    about an individual scheduled Google Meet room
    """

    def __init__(self, room):
        super().__init__()

        self.room = room

        self.setObjectName("main")
        self.setStyleSheet("""
            QFrame#main {
                background-color: white;
                border: 1px solid gray;
                border-radius: 16;
                margin: 10px;
            }

            QLabel#roomTitle {
                font-size: 20px;
                color: white;
                padding: 6px;
                padding-top: 10px;
                padding-bottom: 10px;
            }    

            QWidget#header {
                background-color: orange;
                border-top-left-radius: 14;
                border-top-right-radius: 14
            }

            QLabel#code, QLabel#time, QLabel#days {
                padding-left: 10px;
                padding-bottom: 2px;
            }

            QLabel#code {
                font-weight: bold;
                padding-top: 6px;
            }
        """)

        self.setFrameStyle(QFrame.StyledPanel)
        self.setFixedWidth(240)
        self.setFixedHeight(150)
        self.setLineWidth(1)
        self.mousePressEvent = self.room_frame_clicked
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.name_label = QLabel(self.room.name)
        self.name_label.setObjectName("roomTitle")

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addWidget(self.name_label)

        self.header_widget = QWidget()
        self.header_widget.setObjectName("header")
        self.header_widget.setLayout(self.vbox)

        self.code_label = QLabel(self.room.code)
        self.code_label.setObjectName("code")
        self.time_label = QLabel(self.room.time)
        self.time_label.setObjectName("time")

        days_string = " ".join(self.room.days_list)

        self.days_label = QLabel(days_string)
        self.days_label.setObjectName("days")

        self.body_vbox = QVBoxLayout()
        self.body_vbox.setContentsMargins(0, 0, 0, 0)
        self.body_vbox.addWidget(self.code_label)
        self.body_vbox.addWidget(self.time_label)
        self.body_vbox.addWidget(self.days_label)

        self.body_widget = QWidget()
        self.body_widget.setObjectName("body")
        self.body_widget.setLayout(self.body_vbox)

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout.addWidget(self.header_widget)
        self.vbox_layout.addWidget(self.body_widget)
        self.vbox_layout.addStretch()

        self.setLayout(self.vbox_layout)

    def room_frame_clicked(self, mouse_click):
        # creates instance of EditRoomWindow for its own
        self.edit_room_window = EditRoomWindow(self)

        point = QPoint(50, 50)
        global_point = self.parent().mapToGlobal(point)
        self.edit_room_window.move(global_point)
        self.edit_room_window.show()

        # sets up inputs to based on EditRoomFrame's labels' texts
        self.edit_room_window.name_input.setText(self.room.name)
        self.edit_room_window.code_input.setText(self.room.code)

        time = QTime.fromString(self.room.time, "h:mm AP")
        self.edit_room_window.time_input.setTime(time)

        self.edit_room_window.days_input.check_buttons(self.room.days_list)


class AddRoomFrame(QFrame):
    """
    clickable frame used for adding new EditRoomFrame instances to MainWindow
    """

    def __init__(self):
        super().__init__()

        self.setFrameStyle(QFrame.StyledPanel)
        self.setFixedWidth(240)
        self.setFixedHeight(150)
        self.setLineWidth(1)
        self.mousePressEvent = self.add_room_clicked
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setObjectName("main")

        self.setStyleSheet("""
        QFrame#main {
                background-color: white;
                border: 1px solid gray;
                border-radius: 16;
                margin: 10px;
            }

        QLabel#icon {
                font-size: 30px
            }
        """)

        self.add_icon_label = QLabel("+")
        self.add_icon_label.setObjectName("icon")
        self.add_room_label = QLabel("Add Room")

        self.add_room_frame_layout = QVBoxLayout()
        self.add_room_frame_layout.addStretch()
        self.add_room_frame_layout.addWidget(self.add_icon_label, alignment=Qt.AlignHCenter)
        self.add_room_frame_layout.addWidget(self.add_room_label, alignment=Qt.AlignHCenter)
        self.add_room_frame_layout.addStretch()

        self.setLayout(self.add_room_frame_layout)

    def add_room_clicked(self, mouse_click):
        # opens AddFrameWindow which gets information about a room
        self.add_room_window = AddRoomWindow()

        point = QPoint(50, 50)
        global_point = self.parentWidget().mapToGlobal(point)

        self.add_room_window.move(global_point)
        self.add_room_window.show()


class DaysWidget(QWidget):
    """
    custom widget containing the 7 days of a week as toggleable buttons
    """

    def __init__(self):
        super().__init__()
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(False)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        days = ["M", "T", "W", "Th", "F", "Sa", "Su"]
        for i in range(len(days)):
            day_button = QPushButton(days[i])
            self.button_group.addButton(day_button, i)
            day_button.setObjectName("day")
            day_button.setCheckable(True)
            day_button.clicked.connect(lambda: self.change_color(day_button))
            hbox.addWidget(day_button)

        self.setLayout(hbox)

    @staticmethod
    def change_color(button):

        if button.isChecked():
            button.setStyleSheet("background-color: light blue")
        else:
            button.setStyleSheet("background-color: light gray")

    def checked_buttons_text(self):
        """returns a list of the days which were checked"""

        days = []
        for button in self.button_group.buttons():
            if button.isChecked():
                days.append(button.text())

        return days

    def check_buttons(self, days_list):
        """checks the buttons corresponding to the days given from a list"""

        buttons = self.button_group.buttons()

        for i in range(len(days_list)):
            for j in range(len(buttons)):
                if buttons[j].text() == days_list[i]:
                    buttons[j].setChecked(True)


class RoomWindow(QWidget):
    """
    super class for EditRoomWindow and AddRoomWindow because they look
    the same except for the delete button found in the top right corner
    """

    def __init__(self, header_title):
        super().__init__()

        self.header_title = header_title
        self.setObjectName("main")
        self.setStyleSheet("""
            QWidget#main {
                background-color: white;
                border: 1px solid gray;
            }

            QLabel#head {
                font-size: 20px;
            }

            QPushButton#day {
                background-color: light gray;
            }
        """)

        self.setAttribute(Qt.WA_StyledBackground)

        self.setFixedSize(QSize(400, 300))
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        # locks main window until user exits info widget
        self.setWindowModality(Qt.ApplicationModal)

        self.create_contents()

    def create_contents(self):

        # HEADER SECTION
        self.head_label = QLabel(self.header_title)
        self.head_label.setMaximumHeight(20)
        self.head_label.setObjectName("head")

        self.delete_room_button = QPushButton()
        self.delete_room_button.setMaximumWidth(30)

        style = self.delete_room_button.style()
        icon = style.standardIcon(QStyle.SP_DialogDiscardButton)
        self.delete_room_button.setIcon(icon)

        # button is hidden by default
        self.delete_room_button.hide()

        self.head_hbox = QHBoxLayout()
        self.head_hbox.addWidget(self.head_label)
        self.head_hbox.addWidget(self.delete_room_button)

        # FORM SECTION
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        self.code_label = QLabel("Code:")
        self.code_input = QLineEdit()

        self.time_label = QLabel("Time:")
        self.time_input = QTimeEdit()

        self.room_day_label = QLabel("Days:")
        self.days_input = DaysWidget()

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(20)
        form_layout.addRow(self.name_label, self.name_input)
        form_layout.addRow(self.code_label, self.code_input)
        form_layout.addRow(self.time_label, self.time_input)
        form_layout.addRow(self.room_day_label, self.days_input)

        # BOTTOM SECTION
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_info)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close_window)

        button_hbox = QHBoxLayout()
        button_hbox.addWidget(save_button)
        button_hbox.addWidget(cancel_button)

        # OVERALL LAYOUT
        vbox = QVBoxLayout()
        vbox.addSpacing(4)
        vbox.addLayout(self.head_hbox)
        vbox.addSpacing(40)
        vbox.addLayout(form_layout)
        vbox.addLayout(button_hbox)

        self.setLayout(vbox)

    def save_info(self):
        room = self.get_room_object()

    def get_room_object(self):

        name = self.name_input.text()
        code = self.code_input.text()
        time = self.time_input.text()
        days_list = self.days_input.checked_buttons_text()

        room = Room(name, code, time, days_list)

        return room

    @staticmethod
    def get_position(count):
        """
        finds position to add frame to grid layout (2 column grid)
        :param count: nth widget to be added
        :return: position tuple
        """

        row = math.ceil(count / 2) - 1

        num = count / 2

        if num.is_integer():
            column = 1
        else:
            column = 0

        position = (row, column)

        return position

    def close_window(self):
        self.hide()


class EditRoomWindow(RoomWindow):

    def __init__(self, edit_room_frame):

        header_title = "Edit Room Info: "
        super().__init__(header_title)
        self.edit_room_frame = edit_room_frame
        self.delete_room_button.clicked.connect(self.delete_frame)

        self.delete_room_button.show()

    def save_info(self):
        name = self.edit_room_frame.name_label.text()
        code = self.edit_room_frame.code_label.text()
        time = self.edit_room_frame.time_label.text()
        days = self.edit_room_frame.days_label.text()

        old_room = Room(name, code, time, days)
        new_room = self.get_room_object()

        window.database.update_room(old_room, new_room)

        # Updates attributes of EditRoomFrame instance
        self.edit_room_frame.room = new_room

        # Updates labels of EditRoomFrame instance
        self.edit_room_frame.name_label.setText(new_room.name)
        self.edit_room_frame.code_label.setText(new_room.code)
        self.edit_room_frame.time_label.setText(new_room.time)
        self.edit_room_frame.days_label.setText(Room.days_strflist(new_room.days_list))

        self.close_window()

    def delete_frame(self):

        # deletes current EditRoomFrame but leaves a 'hole' in the GridLayout
        self.edit_room_frame.deleteLater()

        room = self.edit_room_frame.room
        window.database.delete_room(room)

        # gets list of all EditRoomFrame instances in MainWindow
        parent_widget = self.edit_room_frame.parentWidget()
        edit_room_frames_list = parent_widget.findChildren(EditRoomFrame)
        edit_room_frames_list.remove(self.edit_room_frame)

        # deletes all EditRoomFrame instances and re-adds all of them
        # removing that 'hole' if the deleted frame was in the middle
        for frame in edit_room_frames_list:
            frame.deleteLater()

        add_room_frame = parent_widget.findChild(AddRoomFrame)
        add_room_frame.deleteLater()

        children_count = 1

        for frame in edit_room_frames_list:
            pos = self.get_position(children_count)
            room = frame.room
            window.grid_layout.addWidget(
                EditRoomFrame(room), pos[0], pos[1])
            children_count += 1

        if children_count == 1:
            # blank widget to keep grid with 2 columns at initial
            window.grid_layout.addWidget(QWidget(), 0, 1)

        self.close_window()


class AddRoomWindow(RoomWindow):

    def __init__(self):
        header_title = "Add Room Info: "
        super().__init__(header_title)

    def save_info(self):
        room = self.get_room_object()

        # saves to database
        window.database.save_room(room)

        # adding room frame to window

        edit_frame = EditRoomFrame(room)
        grid_layout = window.grid_layout

        children_count = len(window.findChildren(EditRoomFrame))
        children_count += 1

        pos = self.get_position(children_count)

        # new edit frame simply replaces add room frame
        grid_layout.addWidget(edit_frame, pos[0], pos[1])

        children_count += 1

        self.add_room_frame = AddRoomFrame()
        pos = self.get_position(children_count)
        window.grid_layout.addWidget(self.add_room_frame, pos[0], pos[1])

        self.close_window()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.database = RoomDatabase()

        stylesheet = """
            QScrollArea {
                background-color: white
            }
        """

        self.setFixedHeight(400)
        self.setMinimumWidth(520)
        self.setWindowTitle("Google Meet Auto Joiner")
        self.setStyleSheet(stylesheet)
        self.create_window_contents()

    def create_window_contents(self):

        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setContentsMargins(0, 10, 0, 0)

        rooms = self.database.get_all_rooms()

        children_count = 1

        # rooms is a list containing a room tuple from database
        for room_tuple in rooms:
            room = Room(room_tuple[0], room_tuple[1], room_tuple[2], room_tuple[3])
            edit_room_frame = EditRoomFrame(room)
            pos = self.get_position(children_count)

            self.grid_layout.addWidget(
                edit_room_frame, pos[0], pos[1])
            children_count += 1

        self.add_room_frame = AddRoomFrame()
        pos = self.get_position(children_count)
        self.grid_layout.addWidget(self.add_room_frame, pos[0], pos[1])

        if children_count == 1:
            # blank widget to keep grid with 2 columns at initial
            # if grid contains only 1 room frame only (Add Room only)
            self.grid_layout.addWidget(QWidget(), 0, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(self.grid_layout)
        vbox.addStretch()

        self.central_widget = QWidget()
        self.central_widget.setLayout(vbox)

        self.scroll_area = QScrollArea()
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.central_widget)

        self.setCentralWidget(self.scroll_area)

    @staticmethod
    def get_position(count):
        """
        finds next available position to add frame to grid layout (2 column grid)
        :param count: nth widget to be added
        :return: position tuple
        """

        row = math.ceil(count / 2) - 1

        num = count / 2

        if num.is_integer():
            column = 1
        else:
            column = 0

        position = (row, column)

        return position


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    app.exec()
