import sys
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

from PyQt5.QtCore import QSize, Qt, QTime, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QButtonGroup
from PyQt5.QtWidgets import QPushButton, QListWidget, QListWidgetItem, QFormLayout, QLineEdit, QTimeEdit

from database import RoomDatabase, Room
from schedule import scheduler, open_meet_room


class DaysEdit(QWidget):

    days_of_week_list = ["M", "T", "W", "Th", "F", "S", "Su"]

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.button_group = QButtonGroup()
        self.button_group.setExclusive(False)

        for i in range(len(DaysEdit.days_of_week_list)):
            push_button = QPushButton(DaysEdit.days_of_week_list[i])
            push_button.setFixedWidth(48)
            push_button.setCheckable(True)

            self.button_group.addButton(push_button, i+1)
            self.layout.addWidget(push_button)

    def get_clicked_buttons(self):
        days_list = []

        for button in self.button_group.buttons():
            if button.isChecked():
                days_list.append(button.text())

        if len(days_list) == 0:
            return DaysEdit.days_of_week_list[datetime.today().weekday()]

        else:
            return " ".join(days_list)

    def unclick_all_buttons(self):
        for button in self.button_group.buttons():
            button.setChecked(False)

    def click_buttons(self, days_str):
        days_list = days_str.split()

        for button in self.button_group.buttons():
            if button.text() in days_list:
                button.setChecked(True)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Google Meet Auto Opener")
        self.setMinimumSize(QSize(400, 300))

        self.database = RoomDatabase()
        self.scheduler = scheduler
        self.scheduler.start()

        # header
        self.header_layout = QHBoxLayout()

        self.rooms_list_label = QLabel("Scheduled Rooms: ")
        font = QFont()
        font.setPointSize(12)
        self.rooms_list_label.setFont(font)

        self.header_layout.addWidget(self.rooms_list_label)
        self.header_layout.addStretch()

        self.unselect_button = QPushButton("Unselect")
        self.unselect_button.clicked.connect(self.unselect_list_item)

        self.header_layout.addWidget(self.unselect_button)
        # end header

        # body
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.list_item_clicked)
        # end body

        # footer
        self.footer_layout = QHBoxLayout()

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.enable_form_inputs)
        self.footer_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.enable_form_inputs)
        self.footer_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_list_item)
        self.footer_layout.addWidget(self.delete_button)
        # end footer

        self.action_label = QLabel("Add Room: ")

        font = QFont()
        font.setPointSize(10)
        self.action_label.setFont(font)

        # form
        self.form_layout = QFormLayout()

        self.name_label = QLabel("Name: ")
        self.name_input = QLineEdit()
        self.name_input.setMaxLength(24)

        self.form_layout.addRow(self.name_label, self.name_input)

        self.code_label = QLabel("Code: ")
        self.code_input = QLineEdit()

        regexp = QRegExp(r'[a-zA-Z]{3,3}-[a-zA-Z]{4,4}-[a-zA-Z]{3,3}')
        self.code_input.setValidator(QRegExpValidator(regexp))

        self.form_layout.addRow(self.code_label, self.code_input)

        self.time_label = QLabel("Time: ")
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime(7, 30, 0))

        self.form_layout.addRow(self.time_label, self.time_input)

        self.days_label = QLabel("Days: ")
        self.days_input = DaysEdit()

        self.form_layout.addRow(self.days_label, self.days_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_form_info)
        self.save_button.setFixedWidth(100)
        # end form

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.list_widget)
        self.main_layout.addLayout(self.footer_layout)
        self.main_layout.addSpacing(10)
        self.main_layout.addWidget(self.action_label)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.save_button, alignment=Qt.AlignHCenter)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # setting initial configuration
        self.unselect_button.setEnabled(False)
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.disable_form_inputs()

        rooms = self.database.get_all_rooms()

        for room in rooms:
            self.list_widget.addItem(QListWidgetItem(f"{room.name}   {room.code}   {room.time}   {room.days}"))

    def save_form_info(self):
        form_inputs = self.get_form_inputs()

        new_room = Room(form_inputs[0], form_inputs[1], form_inputs[2], form_inputs[3])

        if self.add_button.isEnabled():
            self.list_widget.addItem(QListWidgetItem(
                f"{new_room.name}   {new_room.code}   {new_room.time}   {new_room.days}"))

            self.database.save_room(new_room)

            self.create_job_from_room(new_room)
            self.clear_form_inputs()

        else:
            item = self.list_widget.currentItem()
            name, code, time, days = item.text().split("   ")
            old_room = Room(name, code, time, days)

            self.list_widget.currentItem().setText(
                f"{new_room.name}   {new_room.code}   {new_room.time}   {new_room.days}")

            self.database.edit_room(old_room, new_room)

            # deleting old job then adding edited job
            job_id = f"{old_room.name}_{old_room.code}_{old_room.time}_{old_room.days}"
            scheduler.remove_job(job_id=job_id)

            self.create_job_from_room(new_room)

        self.disable_form_inputs()

    def get_form_inputs(self):
        name = self.name_input.text().strip()
        code = self.code_input.text().strip()
        time = self.time_input.text().strip()
        days = self.days_input.get_clicked_buttons()

        return [name, code, time, days]

    def clear_form_inputs(self):

        self.name_input.clear()
        self.code_input.clear()
        self.time_input.setTime(QTime(7, 30, 0))
        self.days_input.unclick_all_buttons()

    def disable_form_inputs(self):
        self.name_input.setEnabled(False)
        self.code_input.setEnabled(False)
        self.time_input.setEnabled(False)
        self.days_input.setEnabled(False)

        self.save_button.setEnabled(False)

    def enable_form_inputs(self):
        self.name_input.setEnabled(True)
        self.code_input.setEnabled(True)
        self.time_input.setEnabled(True)
        self.days_input.setEnabled(True)

        self.save_button.setEnabled(True)

    def set_form_inputs(self, name, code, time, days):
        self.name_input.setText(name)
        self.code_input.setText(code)

        time = QTime.fromString(time, "h:mm AP")
        self.time_input.setTime(time)

        self.days_input.click_buttons(days)

    def list_item_clicked(self):
        self.add_button.setEnabled(False)
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.unselect_button.setEnabled(True)
        self.action_label.setText("Edit Room:")

        item = self.list_widget.currentItem()
        name, code, time, days = item.text().split("   ")
        self.clear_form_inputs()
        self.set_form_inputs(name, code, time, days)

        self.disable_form_inputs()
        self.disable_form_inputs()

    def unselect_list_item(self):
        self.list_widget.clearSelection()

        self.action_label.setText("Add room:")
        self.add_button.setEnabled(True)
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.unselect_button.setEnabled(False)

        self.clear_form_inputs()

    def delete_list_item(self):
        item = self.list_widget.currentItem()
        name, code, time, days = item.text().split("   ")
        room = Room(name, code, time, days)

        item_index = self.list_widget.currentRow()
        self.list_widget.clearSelection()
        self.list_widget.takeItem(item_index)

        self.database.delete_room(room)

        # deleting job from scheduler
        job_id = f"{room.name}_{room.code}_{room.time}_{room.days}"
        self.scheduler.remove_job(job_id=job_id)

        self.clear_form_inputs()

        if self.list_widget.count() == 0:
            self.action_label.setText("Add room:")
            self.add_button.setEnabled(True)
            self.edit_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.unselect_button.setEnabled(False)
            self.disable_form_inputs()

        else:
            item = self.list_widget.currentItem()
            name, code, time, days = item.text().split("   ")
            self.set_form_inputs(name, code, time, days)

    def create_job_from_room(self, room):

        time_obj = QTime.fromString(room.time, "h:mm AP")

        days_of_week_str = room.days_longstr

        trigger = CronTrigger(day_of_week=days_of_week_str, hour=time_obj.hour(), minute=time_obj.minute())

        job_id = f"{room.name}_{room.code}_{room.time}_{room.days}"
        job = self.scheduler.add_job(open_meet_room, args=[room.code],
                                     trigger=trigger, id=job_id,
                                     misfire_grace_time=10)

    def closeEvent(self, event):
        self.database.close()


if __name__ == '__main__':
    from base import application_context

    window = MainWindow()
    window.show()
    exit_code = application_context.app.exec_()
    sys.exit(exit_code)
