from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QLabel, QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QStyle, QTimeEdit, QButtonGroup
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtGui import QCursor
import sys


# TODO: dynamically add EditRoomFrame after a room is created in AddRoomWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        stylesheet = """
        
            QMainWindow {
                background-color: white;
            }
                        
        """

        self.setFixedSize(QSize(500, 400))
        self.setWindowTitle("Google Meet Auto Joiner")
        self.setStyleSheet(stylesheet)

        self.create_window_contents()

    def create_window_contents(self):

        self.room_frame = EditRoomFrame()
        self.add_room_frame = AddRoomFrame()

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


class EditRoomFrame(QFrame):

    def __init__(self):
        super().__init__()

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
        self.setMaximumWidth(240)
        self.setMaximumHeight(150)
        self.setLineWidth(1)
        self.mousePressEvent = self.room_frame_clicked
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.room_title_label = QLabel("Physics")
        self.room_title_label.setObjectName("roomTitle")

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addWidget(self.room_title_label)

        self.room_header_widget = QWidget()
        self.room_header_widget.setObjectName("header")
        self.room_header_widget.setLayout(self.vbox)

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

        self.frame_layout = QVBoxLayout()
        self.frame_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_layout.addWidget(self.room_header_widget)
        self.frame_layout.addWidget(self.room_body_widget)
        self.frame_layout.addStretch()

        self.setLayout(self.frame_layout)

    def room_frame_clicked(self, mouse_click):

        self.edit_room_window = EditRoomWindow()

        point = QPoint(50, 50)
        global_point = self.parent().mapToGlobal(point)
        self.edit_room_window.move(global_point)
        self.edit_room_window.show()


class AddRoomFrame(QFrame):

    def __init__(self):
        super().__init__()

        self.setFrameStyle(QFrame.StyledPanel)
        self.setMaximumWidth(240)
        self.setMaximumHeight(150)
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


class EditRoomWindow(RoomWindow):

    def __init__(self):

        header_title = "Edit Room Info: "
        super().__init__(header_title)

        self.delete_room_button.show()


class AddRoomWindow(RoomWindow):

    def __init__(self):
        header_title = "Add Room Info: "
        super().__init__(header_title)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

