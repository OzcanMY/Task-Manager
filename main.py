import sys
from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QGridLayout, \
    QLabel, QHBoxLayout, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QHeaderView


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class Task:
    def __init__(self):
        self.task_building_date = ""
        self.task_previs_finish_date = ""
        self.task_last_mod_date = ""
        self.task_priority_level = ""
        self.task_description = ""
        self.task_hardware = ""
        self.task_status = ""
        self.task_comment = ""


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumWidth(330)
        self.setWindowTitle("Mission Manager")
        self.b_new_task = QPushButton("Nouvelle tâche")
        self.b_new_task.clicked.connect(new_task)
        self.b_task_base = QPushButton("Base de tâches")
        self.b_task_base.clicked.connect(task_base)
        layout = QVBoxLayout()
        layout.addWidget(self.b_new_task)
        layout.addWidget(self.b_task_base)
        self.setLayout(layout)
        self.show()


def new_task():
    global w_new_task
    w_new_task = NewTaskWindow()


class TaskBase(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Base de missions")
        self.show()


class NewTaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nouvelle mission")
        self.tb_description_box = QTextEdit()
        self.tb_description_box.setAcceptRichText(True)
        self.b_validate = QPushButton("Valider")
        self.b_validate.clicked.connect(self.task_builder)
        self.lb_build_date = QLabel("Date du ticket")
        self.de_build_date = QLabel(datetime.today().strftime('%d/%m/%Y'))
        self.lb_status = QLabel("Statut")
        self.cb_status = QComboBox()
        self.cb_status.addItem("TBD")
        self.cb_status.addItem("ON")
        self.lb_previs_date = QLabel("Date de fin prévisionnelle")
        self.de_previs_date = QDateEdit(calendarPopup=True)
        self.de_previs_date.setDateTime(datetime.today())
        self.lb_prio_level = QLabel("Priorité")
        self.cb_prio_level = QComboBox()
        self.cb_prio_level.addItem("U")
        self.cb_prio_level.addItem("A")
        self.lb_hardware = QLabel("Moyen")
        self.t_hardware = QLineEdit()
        self.b_add_comment = QPushButton("Ajouter un commentaire")
        self.b_add_comment.clicked.connect(add_a_comment)
        self.l_left_layout = QVBoxLayout()
        self.l_left_layout.addWidget(self.tb_description_box)
        self.l_left_layout.addWidget(self.b_validate)
        self.l_right_layout = QVBoxLayout()
        self.l_right_layout.addWidget(self.lb_build_date)
        self.l_right_layout.addWidget(self.de_build_date)
        self.l_right_layout.addWidget(self.lb_status)
        self.l_right_layout.addWidget(self.cb_status)
        self.l_right_layout.addWidget(self.lb_previs_date)
        self.l_right_layout.addWidget(self.de_previs_date)
        self.l_right_layout.addWidget(self.lb_prio_level)
        self.l_right_layout.addWidget(self.cb_prio_level)
        self.l_right_layout.addWidget(self.lb_hardware)
        self.l_right_layout.addWidget(self.t_hardware)
        self.l_right_layout.addWidget(self.b_add_comment)
        self.l_right_layout.addStretch()
        self.l_pseudo_widget = QWidget()
        self.l_pseudo_widget.setLayout(self.l_right_layout)
        self.l_pseudo_widget.setMaximumWidth(200)
        self.l_layout = QHBoxLayout()
        self.l_layout.addLayout(self.l_left_layout)
        self.l_layout.addWidget(self.l_pseudo_widget)
        self.setLayout(self.l_layout)
        self.show()

    def task_builder(self):
        newTask = Task()
        newTask.task_building_date = self.de_build_date.text()
        newTask.task_previs_finish_date = self.de_previs_date.text()
        newTask.task_status = self.cb_status.currentText()
        newTask.task_description = self.tb_description_box.toPlainText()
        newTask.task_hardware = self.t_hardware.text()
        newTask.task_priority_level = self.cb_prio_level.currentText()
        #newTask.task_comment =
        add_task_to_tb(newTask)


def add_task_to_tb(task):
    global table
    table = QTableWidget(3, 6)
    table.setHorizontalHeaderLabels(["Date ticket", "Date prévis", "Prio", "Statut", "Description", "Moyen"])
    table.setAlternatingRowColors(True)
    # table.setStyleSheet("background-color: red")
    table.setItem(0, 0, QTableWidgetItem(task.task_building_date))
    table.setItem(0, 1, QTableWidgetItem(task.task_previs_finish_date))
    table.setItem(0, 2, QTableWidgetItem(task.task_priority_level))
    table.setItem(0, 3, QTableWidgetItem(task.task_status))
    table.setItem(0, 4, QTableWidgetItem(task.task_description))
    table.setItem(0, 5, QTableWidgetItem(task.task_hardware))
    table.resizeRowsToContents()
    table.setSizeAdjustPolicy(2)    # Adjust window size to table's one. "2" : Adjust to content from Qt documentation
    delegate = AlignDelegate(table)
    table.setItemDelegateForColumn(0, delegate)
    table.setItemDelegateForColumn(1, delegate)
    table.setItemDelegateForColumn(2, delegate)
    table.setItemDelegateForColumn(3, delegate)
    table.show()
    print(task.task_comment)

class CommentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(330)
        self.setWindowTitle("Commentaire")
        self.tb_comment = QTextEdit()
        self.b_validate = QPushButton("Valider")
        self.b_validate.clicked.connect(add_comment(self.tb_comment.toPlainText()))
        self.l_layout = QVBoxLayout()
        self.l_layout.addWidget(self.tb_comment)
        self.l_layout.addWidget(self.b_validate)
        self.setLayout(self.l_layout)
        self.show()

def add_comment(task):
    w_new_task.task_comment = task.tb_comment


def add_a_comment():
    global w_comment
    w_comment = CommentWindow()


def task_base():
    global w_task_base
    w_task_base = TaskBase()
    print("OK")


app = QApplication(sys.argv)
fen = MainWindow()
fen.show()
app.exec_()
