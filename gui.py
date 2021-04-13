from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QLabel, QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QStyle, QTimeEdit, QButtonGroup
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtGui import QCursor
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        stylesheet = """
            QMainWindow {
                background-color: white;
            }
            
            .QFrame {
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
            
            QLabel#icon {
                font-size: 30px
            }
            
            QWidget#info {
                background-color: blue
            }
            
        """

        self.setFixedSize(QSize(500, 400))
        self.setWindowTitle("Google Meet Auto Joiner")
        self.setStyleSheet(stylesheet)

        self.create_window_contents()

    def create_window_contents(self):

        self.add_icon_label = QLabel("+")
        self.add_icon_label.setObjectName("icon")
        self.add_room_label = QLabel("Add Room")

        self.add_room_frame_layout = QVBoxLayout()
        self.add_room_frame_layout.addStretch()
        self.add_room_frame_layout.addWidget(self.add_icon_label, alignment=Qt.AlignHCenter)
        self.add_room_frame_layout.addWidget(self.add_room_label, alignment=Qt.AlignHCenter)
        self.add_room_frame_layout.addStretch()

        self.add_room_frame = QFrame()
        self.add_room_frame.setFrameStyle(QFrame.StyledPanel)
        self.add_room_frame.setMaximumWidth(240)
        self.add_room_frame.setMaximumHeight(150)
        self.add_room_frame.setLineWidth(1)
        self.add_room_frame.setLayout(self.add_room_frame_layout)
        self.add_room_frame.mousePressEvent = self.add_room_clicked
        self.add_room_frame.setCursor(QCursor(Qt.PointingHandCursor))

        # ROOM
        # HEADER
        self.room_title_label = QLabel("Physics")
        self.room_title_label.setObjectName("roomTitle")

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addWidget(self.room_title_label)

        self.room_header_widget = QWidget()
        self.room_header_widget.setObjectName("header")
        self.room_header_widget.setLayout(self.vbox)
        # END Of HEADER

        # BODY
        self.room_code_label = QLabel("xxx-yyyy-zzz")
        self.room_code_label.setObjectName("code")
        self.room_time_label = QLabel("7:30 AM")
        self.room_time_label.setObjectName("time")
        self.room_day_label = QLabel("M T W Th F Sa Su")
        self.room_day_label.setObjectName("days")

        self.body_vbox = QVBoxLayout()
        self.body_vbox.setContentsMargins(0, 0, 0, 0)
        self.body_vbox.addWidget(self.room_code_label)
        self.body_vbox.addWidget(self.room_time_label)
        self.body_vbox.addWidget(self.room_day_label)

        self.room_body_widget = QWidget()
        self.room_body_widget.setObjectName("body")
        self.room_body_widget.setLayout(self.body_vbox)
        # END OF BODY

        self.frame_layout = QVBoxLayout()
        self.frame_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_layout.addWidget(self.room_header_widget)
        self.frame_layout.addWidget(self.room_body_widget)
        self.frame_layout.addStretch()

        self.room_frame = QFrame()
        self.room_frame.setFrameStyle(QFrame.StyledPanel)
        self.room_frame.setMaximumWidth(240)
        self.room_frame.setMaximumHeight(150)
        self.room_frame.setLineWidth(1)
        self.room_frame.setLayout(self.frame_layout)
        self.room_frame.mousePressEvent = self.room_frame_clicked
        self.room_frame.setCursor(QCursor(Qt.PointingHandCursor))

        self.room_frame.setFrameShadow(10)

        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setContentsMargins(0, 10, 0, 0)

        self.grid_layout.addWidget(self.room_frame, 0, 0)
        self.grid_layout.addWidget(self.add_room_frame, 0, 1)
        self.grid_layout.addWidget(QWidget(), 1, 0)

        self.center_widget = QWidget()
        self.center_widget.setObjectName("center")
        self.center_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.center_widget)

    def room_frame_clicked(self, mouse_click):
        print("Room Clicked")

        self.info_widget = QWidget()
        self.info_widget.setObjectName("info")

        self.info_widget.setStyleSheet("""
            
            QWidget#info {
                background-color: white;
                border: 1px solid gray
            }
            
            QLabel#head {
                font-size: 20px;
            }
            
            QPushButton#day {
                background-color: light gray;
            }
            
        """)

        self.info_widget.setFixedSize(QSize(400, 300))
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.info_widget.setWindowFlags(flags)

        point = QPoint(50, 50)
        global_point = self.mapToGlobal(point)

        self.info_widget.move(global_point)

        head_label = QLabel("Edit Room Info:")
        head_label.setObjectName("head")

        delete_room_button = QPushButton()
        delete_room_button.setMaximumWidth(30)

        style = delete_room_button.style()
        icon = style.standardIcon(QStyle.SP_DialogDiscardButton)
        delete_room_button.setIcon(icon)

        head_hbox = QHBoxLayout()
        head_hbox.addWidget(head_label)
        head_hbox.addWidget(delete_room_button)

        room_name_label = QLabel("Room Name: ")
        room_name_input = QLineEdit()

        room_code_label = QLabel("Room Code: ")
        room_code_input = QLineEdit()

        room_time_label = QLabel("Room Time: ")
        room_time_input = QTimeEdit()

        room_day_label = QLabel("Room Day: ")

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        days = ["M", "T", "W", "Th", "F", "Sa", "Su"]
        for day in days:
            day_button = QPushButton(day)
            day_button.setObjectName("day")
            day_button.setCheckable(True)
            day_button.clicked.connect(lambda: self.change_color(day_button))
            hbox.addWidget(day_button)

        days_button_group = QWidget()
        days_button_group.setLayout(hbox)

        room_day_input = days_button_group

        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(10)
        form_layout.addRow(room_name_label, room_name_input)
        form_layout.addRow(room_code_label, room_code_input)
        form_layout.addRow(room_time_label, room_time_input)
        form_layout.addRow(room_day_label, room_day_input)

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close_info_widget)

        button_hbox = QHBoxLayout()
        button_hbox.addWidget(save_button)
        button_hbox.addWidget(cancel_button)

        vbox = QVBoxLayout()
        vbox.addSpacing(4)
        vbox.addLayout(head_hbox)
        vbox.addSpacing(40)
        vbox.addLayout(form_layout)
        vbox.addLayout(button_hbox)

        self.info_widget.setLayout(vbox)

        # locks main window until user exits info widget
        self.info_widget.setWindowModality(Qt.ApplicationModal)
        self.info_widget.show()

    def change_color(self, button):

        if button.isChecked():
            button.setStyleSheet("background-color: light blue")
        else:
            button.setStyleSheet("background-color: light gray")

    def add_room_clicked(self, mouse_click):
        print("Add Room")

        self.add_room_window = AddRoomWindow()

        point = QPoint(50, 50)
        global_point = self.mapToGlobal(point)
        self.add_room_window.move(global_point)

        self.add_room_window.show()

    def save_info(self):
        room = self.get_info()

        print("Saving Info...")
        print(f"Room Name: {room['room_name']}")
        print(f"Room Code: {room['room_code']}")
        print(f"Room Time: {room['room_time']}")

    def get_info(self):
        inputs = self.info_widget.findChildren(QLineEdit)

        for button in self.button_group.buttons():
            if button.isChecked():
                print(button.text())

        room = {
            "room_name": inputs[0].text(),
            "room_code": inputs[1].text(),
            "room_time": inputs[2].text(),
        }

        return room

    def close_info_widget(self):
        self.info_widget.hide()


class AddRoomWindow(QWidget):

    def __init__(self):
        super().__init__()

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

        head_label = QLabel("Create Room:")
        head_label.setMaximumHeight(20)
        head_label.setObjectName("head")

        head_hbox = QHBoxLayout()
        head_hbox.addWidget(head_label)

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
        print(f"Room Name: {room['room_name']}")
        print(f"Room Code: {room['room_code']}")
        print(f"Room Time: {room['room_time']}")
        print(f"Room Days: {room['room_days']}")

    def get_info(self):
        inputs = self.findChildren(QLineEdit)

        days = []
        for button in self.button_group.buttons():
            if button.isChecked():
                days.append(button.text())

        room = {
            "room_name": self.room_name_input.text(),
            "room_code": self.room_code_input.text(),
            "room_time": self.room_time_input.text(),
            "room_days": days
        }

        return room

    def close_window(self):
        self.hide()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

