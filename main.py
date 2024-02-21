import sys
import os
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QGridLayout, \
    QLabel, QHBoxLayout, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QHeaderView, \
    QAbstractScrollArea


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class Task:
    task_inst_db = []
    def __init__(self):
        self.task_token = ""
        self.task_build_date = ""
        self.task_previs_finish_date = ""
        self.task_last_mod_date = ""
        self.task_priority_level = ""
        self.task_hardware = ""
        self.task_status = ""
        self.task_description = ""
        self.task_comment = ""
        Task.task_inst_db.append(self)


class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumWidth(330)
        self.setWindowTitle("Mission Manager")
        self.b_new_task = QPushButton("Nouvelle tâche")
        self.b_new_task.clicked.connect(new_task)
        self.b_task_base = QPushButton("Base de tâches")
        self.b_task_base.clicked.connect(show_task_base)
        layout = QVBoxLayout()
        layout.addWidget(self.b_new_task)
        layout.addWidget(self.b_task_base)
        self.setLayout(layout)
        self.show()


class TaskBaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizeAdjustPolicy(2)
        self.setWindowTitle("Base de missions")
        self.layout = QVBoxLayout()
        self.layout.addWidget(task_base)
        self.setLayout()
        self.show()
    
    def add_task_to_tb(self, task_base):
        idx = task_base.rowCount()
        task_base.insertRow(idx)
        task_base.setHorizontalHeaderLabels(["Date ticket", "Date prévis", "Prio", "Statut", "Description", "Moyen",
                                        "Commentaires"])
        task_base.setAlternatingRowColors(True)
        # task_base.setStyleSheet("background-color: red")
        task_base.setItem(idx, 0, QTableWidgetItem(self.task_build_date))
        task_base.setItem(idx, 1, QTableWidgetItem(self.task_previs_finish_date))
        task_base.setItem(idx, 2, QTableWidgetItem(self.task_priority_level))
        task_base.setItem(idx, 3, QTableWidgetItem(self.task_status))
        task_base.setItem(idx, 4, QTableWidgetItem(self.task_description))
        task_base.setItem(idx, 5, QTableWidgetItem(self.task_hardware))
        task_button = QPushButton("Commentaires")
        task_base.setCellWidget(idx, 6, task_button)
        task_button.show()
        # task_base.resizeRowsToContents()
        # task_base.resizeColumnsToContents()
        # task_base.setSizeAdjustPolicy(2)    # Adjust window size to task_base's one. "2" : Adjust to content from Qt documentation
        # delegate = AlignDelegate(task_base)
        # task_base.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        # task_base.setItemDelegateForColumn(0, delegate)
        # task_base.setItemDelegateForColumn(1, delegate)
        # task_base.setItemDelegateForColumn(2, delegate)
        # task_base.setItemDelegateForColumn(3, delegate)


class NewTaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nouvelle mission")
        self.token = self.generate_token()
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

    def generate_token(self):
        nb_task_in_db = len(Task.task_inst_db)
        return 'OY' + str(nb_task_in_db)

    def task_builder(self):
        newTask = Task()
        newTask.task_token = self.token
        newTask.task_build_date = self.de_build_date.text()
        newTask.task_previs_finish_date = self.de_previs_date.text()
        newTask.task_last_mod_date = ""
        newTask.task_priority_level = self.cb_prio_level.currentText()
        newTask.task_hardware = self.t_hardware.text()
        newTask.task_status = self.cb_status.currentText()
        newTask.task_description = self.tb_description_box.toPlainText()
        try:
            newTask.task_comment = comment
        except:
            newTask.task_comment = ""
        TaskBaseWindow.add_task_to_tb(newTask, task_base)
        task_file = open("{}.task".format(self.token), "w")
        task_file.write('{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n'
                        .format(newTask.task_token, newTask.task_build_date, 
                                newTask.task_previs_finish_date, newTask.task_last_mod_date,
                                newTask.task_priority_level, newTask.task_hardware,
                                newTask.task_status, newTask.task_description,))
        show_task_base()


class NewCommentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(330)
        self.setWindowTitle("Commentaire")
        self.tb_comment = QTextEdit()
        self.b_validate = QPushButton("Valider")
        self.b_validate.clicked.connect(get_comment)
        self.l_layout = QVBoxLayout()
        self.l_layout.addWidget(self.tb_comment)
        self.l_layout.addWidget(self.b_validate)
        self.setLayout(self.l_layout)
        self.show()


def load_task_db():
    os.chdir('db')
    task_list = os.listdir()
    nb_task_in_db = len(os.listdir())
    for task_file in task_list:
        read_task = Task()
        task_file = open(task_file, 'r')
        task_file_content = task_file.read().split('\n')
        try:
            read_task.task_token                = task_file_content[0]
            read_task.task_build_date           = task_file_content[1]
            read_task.task_previs_finish_date   = task_file_content[2]
            read_task.task_last_mod_date        = task_file_content[3]
            read_task.task_priority_level       = task_file_content[4]
            read_task.task_description          = task_file_content[5]
            read_task.task_hardware             = task_file_content[6]
            read_task.task_status               = task_file_content[7]
            read_task.task_comment              = task_file_content[8]
            read_task.task_id                   = task_file_content[9]
        except:
            continue

def new_task():
    global w_new_task
    w_new_task = NewTaskWindow()

def get_comment():
    global comment, w_comment
    comment = w_comment.tb_comment.toPlainText()
    w_comment.close()

def add_a_comment():
    global w_comment, comment
    w_comment = NewCommentWindow()

def show_task_base():
    task_base.setRowCount(0)
    for task in Task.task_inst_db:
        TaskBaseWindow.add_task_to_tb(task, task_base)
    task_base.adjustSize()
    task_base.show()


load_task_db()
app = QApplication(sys.argv)
task_base = QTableWidget(0, 7)
task_base.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
fen = MainWindow()
fen.show()
app.exec_()
