import sys
import os
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QGridLayout, \
    QLabel, QHBoxLayout, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QHeaderView, \
    QAbstractScrollArea


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
        self.task_comment = list()
        Task.task_inst_db.append(self)

    def generate_token(self):
        nb_task_in_db = len(Task.task_inst_db)
        self.task_token = 'OY' + str(nb_task_in_db)

    def add_comment_to_task(self, content):
        self.comment.append(TaskComment(content))


class TaskComment:
    def __init__(self, content):
        self.build_date = ""
        self.content = content
        self.number = ""


class TaskBase(QWidget):
    def __init__(self):
        super().__init__()        
        self.setWindowTitle("Base de missions")
        self.table = QTableWidget(0, 7)
        self.pb_add_new_task = QPushButton('Add new Task')
        self.pb_add_new_task.clicked.connect(self.add_new_row)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
    
    def build(self):
        for task in Task.task_inst_db:
            self.add_task_to_tb(task)
        self.layout.addWidget(self.pb_add_new_task)
        self.setLayout(self.layout)  

    def add_task_to_tb(self, task):
        idx =self.table.rowCount()
        self.table.insertRow(idx)
        self.table.setHorizontalHeaderLabels(["Date ticket", "Date prévis", "Prio", "Statut", "Description", "Moyen",
                                        "Commentaires"])
        self.table.setAlternatingRowColors(True)
        #self.setStyleSheet("background-color: red")
        self.table.setItem(idx, 0, QTableWidgetItem(task.task_build_date))
        self.table.setItem(idx, 1, QTableWidgetItem(task.task_previs_finish_date))
        self.table.setItem(idx, 2, QTableWidgetItem(task.task_priority_level))
        self.table.setItem(idx, 3, QTableWidgetItem(task.task_status))
        self.table.setItem(idx, 4, QTableWidgetItem(task.task_description))
        self.table.setItem(idx, 5, QTableWidgetItem(task.task_hardware))
        task_comment_button = QPushButton("Commentaires")
        # task_comment_button.clicked.connect(CommentWindow.display_existing_comments(task))
        self.table.setCellWidget(idx, 6, task_comment_button)
        task_comment_button.show()

    def add_new_row(self):
        task = Task()
        task.task_token = task.
        task.task_build_date = datetime.today().strftime('%d/%m/%Y')
        idx = self.table.rowCount()
        self.table.insertRow(idx)
        self.table.setItem(idx, 0, QTableWidgetItem(task.task_build_date))
        pb_task_comment = QPushButton('Commentaires')
        self.table.setCellWidget(idx, 6, pb_task_comment)
        self.adjustSize()

    def show_task_base(self):
        self.show()


class CommentWindow(QWidget):
    def __init__(self, task):
        super().__init__()
        # self.setMinimumWidth(330)
        self.setWindowTitle("Commentaires")
        self.task = task
        self.table = QTableWidget(0, 3, parent=self)
        self.table.insertRow(0)
        self.table.setHorizontalHeaderLabels('Build date', 'Comment', 'Number')
        self.table.setAlternatingRowColors(True)
        self.load_existing_comments(task)
        self.show()

    def display_existing_comments(self, task):
        for idx, elt in enumerate(self.task):
            self.table.insertRow(idx + 1)
            self.table.setItem(idx + 1, 0, QTableWidgetItem(self.task.task_comment[idx].build_date))
            self.table.setItem(idx + 1, 1, QTableWidgetItem(self.task.task_comment[idx].content))
            self.table.setItem(idx + 1, 2, QTableWidgetItem(self.task.task_comment[idx].number))


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


load_task_db()
app = QApplication(sys.argv)
tb = TaskBase()
tb.build()
tb.show()
app.exec_()
