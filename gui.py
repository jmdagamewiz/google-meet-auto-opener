from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QLabel, QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QStyle, QTimeEdit, QButtonGroup, QScrollArea
from PyQt5.QtCore import QSize, Qt, QPoint, QTime
from PyQt5.QtGui import QCursor
import sys

import math


class EditRoomFrame(QFrame):

    def __init__(self, room_title, room_code, room_time, room_days_list):
        super().__init__()

        self.room_title = room_title
        self.room_code = room_code
        self.room_time = room_time
        self.room_days_list = room_days_list

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

        self.room_title_label = QLabel(self.room_title)
        self.room_title_label.setObjectName("roomTitle")

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addWidget(self.room_title_label)

        self.room_header_widget = QWidget()
        self.room_header_widget.setObjectName("header")
        self.room_header_widget.setLayout(self.vbox)

        self.room_code_label = QLabel(self.room_code)
        self.room_code_label.setObjectName("code")
        self.room_time_label = QLabel(self.room_time)
        self.room_time_label.setObjectName("time")

        days_string = " ".join(self.room_days_list)

        self.room_day_label = QLabel(days_string)
        self.room_day_label.setObjectName("days")

        self.body_vbox = QVBoxLayout()
        self.body_vbox.setContentsMargins(0, 0, 0, 0)
        self.body_vbox.addWidget(self.room_code_label)
        self.body_vbox.addWidget(self.room_time_label)
        self.body_vbox.addWidget(self.room_day_label)

        self.room_body_widget = QWidget()
        self.room_body_widget.setObjectName("body")
        self.room_body_widget.setLayout(self.body_vbox)

        self.frame_layout = QVBoxLayout()
        self.frame_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_layout.addWidget(self.room_header_widget)
        self.frame_layout.addWidget(self.room_body_widget)
        self.frame_layout.addStretch()

        self.setLayout(self.frame_layout)

    def room_frame_clicked(self, mouse_click):

        self.edit_room_window = EditRoomWindow(self)

        point = QPoint(50, 50)
        global_point = self.parent().mapToGlobal(point)
        self.edit_room_window.move(global_point)
        self.edit_room_window.show()

        self.edit_room_window.room_name_input.setText(self.room_title)
        self.edit_room_window.room_code_input.setText(self.room_code)

        time = QTime.fromString(self.room_time, "h:mm AP")
        self.edit_room_window.room_time_input.setTime(time)

        buttons = self.edit_room_window.button_group.buttons()

        for i in range(len(self.room_days_list)):
            for j in range(len(buttons)):
                if buttons[j].text() == self.room_days_list[i]:
                    buttons[j].setChecked(True)


class AddRoomFrame(QFrame):

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
        print("Add Room")

        self.add_room_window = AddRoomWindow()

        point = QPoint(50, 50)
        global_point = self.parentWidget().mapToGlobal(point)
        self.add_room_window.move(global_point)

        self.add_room_window.show()


class RoomWindow(QWidget):

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

        head_label = QLabel(self.header_title)
        head_label.setMaximumHeight(20)
        head_label.setObjectName("head")

        self.delete_room_button = QPushButton()
        self.delete_room_button.setMaximumWidth(30)

        style = self.delete_room_button.style()
        icon = style.standardIcon(QStyle.SP_DialogDiscardButton)
        self.delete_room_button.setIcon(icon)

        # button is hidden by default
        self.delete_room_button.hide()

        head_hbox = QHBoxLayout()
        head_hbox.addWidget(head_label)
        head_hbox.addWidget(self.delete_room_button)

        self.room_name_label = QLabel("Room Name: ")
        self.room_name_input = QLineEdit()

        self.room_code_label = QLabel("Room Code: ")
        self.room_code_input = QLineEdit()

        self.room_time_label = QLabel("Room Time: ")
        self.room_time_input = QTimeEdit()

        self.room_day_label = QLabel("Room Day: ")

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(False)

        days = ["M", "T", "W", "Th", "F", "Sa", "Su"]
        for i in range(len(days)):
            day_button = QPushButton(days[i])
            self.button_group.addButton(day_button, i)
            day_button.setObjectName("day")
            day_button.setCheckable(True)
            day_button.clicked.connect(lambda: self.change_color(day_button))
            hbox.addWidget(day_button)

        self.room_day_input = QWidget()
        self.room_day_input.setLayout(hbox)

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)
        form_layout.addRow(self.room_name_label, self.room_name_input)
        form_layout.addRow(self.room_code_label, self.room_code_input)
        form_layout.addRow(self.room_time_label, self.room_time_input)
        form_layout.addRow(self.room_day_label, self.room_day_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_info)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close_window)

        button_hbox = QHBoxLayout()
        button_hbox.addWidget(save_button)
        button_hbox.addWidget(cancel_button)

        vbox = QVBoxLayout()
        vbox.addSpacing(4)
        vbox.addLayout(head_hbox)
        vbox.addSpacing(40)
        vbox.addLayout(form_layout)
        vbox.addLayout(button_hbox)

        self.setLayout(vbox)

        # locks main window until user exits info widget
        self.setWindowModality(Qt.ApplicationModal)

    def change_color(self, button):

        if button.isChecked():
            button.setStyleSheet("background-color: light blue")
        else:
            button.setStyleSheet("background-color: light gray")

    def save_info(self):
        room = self.get_info()

        print("Saving Info...")
        print(f"Room Name: {room['name']}")
        print(f"Room Code: {room['code']}")
        print(f"Room Time: {room['time']}")
        print(f"Room Days: {room['days']}")

    def get_info(self):
        inputs = self.findChildren(QLineEdit)

        days = []
        for button in self.button_group.buttons():
            if button.isChecked():
                days.append(button.text())

        room = {
            "name": self.room_name_input.text(),
            "code": self.room_code_input.text(),
            "time": self.room_time_input.text(),
            "days": days
        }

        return room

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
        room = self.get_info()

        print(room["name"], room["code"], room["time"], room["days"])

        # Updates attributes of EditRoomFrame instance
        self.edit_room_frame.room_title = room["name"]
        self.edit_room_frame.room_code = room["code"]
        self.edit_room_frame.room_time = room["time"]
        self.edit_room_frame.room_days_list = room["days"]

        self.edit_room_frame.room_title_label.setText(room["name"])
        self.edit_room_frame.room_code_label.setText(room["code"])
        self.edit_room_frame.room_time_label.setText(room["time"])

        days_string = " ".join(room["days"])

        self.edit_room_frame.room_day_label.setText(days_string)

        self.close_window()

    def delete_frame(self):
        self.edit_room_frame.deleteLater()

        parent_widget = self.edit_room_frame.parentWidget()

        edit_room_frames_list = parent_widget.findChildren(EditRoomFrame)

        edit_room_frames_list.remove(self.edit_room_frame)

        for frame in edit_room_frames_list:
            frame.deleteLater()

        children_count = 2

        for frame in edit_room_frames_list:
            print(frame.room_title_label.text())

        for frame in edit_room_frames_list:
            pos = self.get_position(children_count)

            room = {
                "name": frame.room_title_label.text(),
                "code": frame.room_code_label.text(),
                "time": frame.room_time_label.text(),
                "days": frame.room_day_label.text().split()
            }

            window.grid_layout.addWidget(
                EditRoomFrame(room["name"], room["code"], room["time"], room["days"]), pos[0], pos[1])
            children_count += 1

        self.close_window()

    @staticmethod
    def get_position(count):

        row = math.ceil(count / 2) - 1

        num = count / 2

        if num.is_integer():
            column = 1
        else:
            column = 0

        position = (row, column)

        return position


class AddRoomWindow(RoomWindow):

    def __init__(self):
        header_title = "Add Room Info: "
        super().__init__(header_title)

    def save_info(self):
        room = self.get_info()

        edit_frame = EditRoomFrame(room["name"], room["code"], room["time"], room["days"])

        grid_layout = window.grid_layout

        children_count = len(window.findChildren(EditRoomFrame))
        children_count += len(window.findChildren(AddRoomFrame))
        children_count += 1

        print(children_count)

        pos = self.get_position(children_count)
        print(pos)

        grid_layout.addWidget(edit_frame, pos[0], pos[1])

        self.close_window()

    @staticmethod
    def get_position(count):

        row = math.ceil(count/2) - 1

        num = count / 2

        if num.is_integer():
            column = 1
        else:
            column = 0

        position = (row, column)

        return position


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

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
        self.add_room_frame = AddRoomFrame()

        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setContentsMargins(0, 10, 0, 0)

        self.grid_layout.addWidget(self.add_room_frame, 0, 0)
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


app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()

