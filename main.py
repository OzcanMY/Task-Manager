import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QGridLayout, \
    QLabel, QHBoxLayout, QComboBox, QDateEdit


class Task:
    def __init__(self):
        self.task_building_date = datetime.today().strftime('%d-%m-%Y')
        self.task_previs_finish_date = ""
        self.task_last_mod_date = ""
        self.task_priority_level = ""
        self.task_description = ""
        self.task_hardware = ""
        self.task_state = ""
        self.task_comment = ""


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumWidth(330)
        self.setWindowTitle("Mission Manager")
        self.b_new_task = QPushButton("Nouvelle tâche")
        self.b_new_task.clicked.connect(self.new_task)
        self.b_task_base = QPushButton("Base de tâches")
        self.b_task_base.clicked.connect(task_base)
        layout = QVBoxLayout()
        layout.addWidget(self.b_new_task)
        layout.addWidget(self.b_task_base)
        self.setLayout(layout)
        self.show()

    def new_task(self):
        task = Task()
        new_task(task)

def new_task(task):
    global w_new_task
    w_new_task = NewTaskWindow(task)

class TaskBase(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Base de missions")
        self.show()


class NewTaskWindow(QWidget):
    def __init__(self, task):
        super().__init__()
        self.setWindowTitle("Nouvelle mission")
        self.tb_description_box = QTextEdit()
        self.b_validate = QPushButton("Valider")
        self.lb_build_date = QLabel("Date du ticket")
        self.de_build_date = QLabel(task.task_building_date)
        self.lb_status = QLabel("Statut")
        self.cb_status = QComboBox()
        self.cb_status.addItem("TBD")
        self.lb_previs_date = QLabel("Date de fin prévisionnelle")
        self.de_previs_date = QDateEdit(calendarPopup=True)
        self.de_previs_date.setDateTime(datetime.today())
        self.lb_prio_level = QLabel("Priorité")
        self.cb_prio_level = QComboBox()
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


class CommentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(330)
        self.setWindowTitle("Commentaire")
        self.tb_comment = QTextEdit()
        self.b_validate = QPushButton("Valider")
        self.l_layout = QVBoxLayout()
        self.l_layout.addWidget(self.tb_comment)
        self.l_layout.addWidget(self.b_validate)
        self.setLayout(self.l_layout)
        self.show()

def add_a_comment():
    global w_comment
    w_comment = CommentWindow()

def task_base():
    global w_task_base
    w_task_base = TaskBase()
    print("OK")


list_to_do_list = []
dic_to_do_list = {"build_date", "previs_date", "last_mod_date", "priority", "description",
                  "hardware", "state", "comment"}

app = QApplication(sys.argv)
fen = MainWindow()
fen.show()
app.exec_()

