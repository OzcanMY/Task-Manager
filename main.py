import sys
import os
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QGridLayout, \
     QLabel, QHBoxLayout, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QHeaderView, \
     QAbstractScrollArea, QMainWindow


class Task:
    task_inst_db = []
    def __init__(self):
        self.task_token = self.generate_token()
        self.task_build_date = ""
        self.task_previs_finish_date = ""
        self.task_last_mod_date = ""
        self.task_priority_level = ""
        self.task_hardware = ""
        self.task_status = ""
        self.task_description = ""
        # self.task_comment = list()
        self.task_comment = []

        Task.task_inst_db.append(self)

    def generate_token(self):
        nb_task_in_db = len(Task.task_inst_db)
        return 'OY' + str(nb_task_in_db)
    
    def add_description(self, description):
        des = ""
        for line in description:
            des = des + line
        self.task_description = des
    
    def add_comment(self, comment):
        # com = ""
        # for line in comment:
        #     com = com + line
        self.add_comment_to_task(comment)

    def add_comment_to_task(self, content):
        for idx, line in enumerate(content):
            if line == '[com]':
                idx_start = idx
            if line == '[/com]':
                split_content = content[idx_start + 1: idx]
                com = TaskComment(split_content, True)
                self.task_comment.append(com)


class TaskComment:
    def __init__(self, content="", read=False):
        self.build_date = datetime.today().strftime('%d/%m/%Y')
        self.content = content
        self.number = ""
        if read:
            self.decode_read_comment()
    
    def decode_read_comment(self):
        for i, line in enumerate(self.content):
            if line[0] == '#':
                content = ""
                self.build_date = line[1:]
                continue
            content = content + line
        self.content = content


class TaskBase(QWidget):
    def __init__(self):
        super().__init__()        
        self.setWindowTitle("Base de missions")
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["Date ticket", "Date prévis", "Prio", "Statut", 
                                              "Description", "Moyen", "Commentaires"])
        self.table.setAlternatingRowColors(True)
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
        #self.setStyleSheet("background-color: red")
        self.table.setItem(idx, 0, QTableWidgetItem(task.task_build_date))
        self.table.setItem(idx, 1, QTableWidgetItem(task.task_previs_finish_date))
        self.table.setItem(idx, 2, QTableWidgetItem(task.task_priority_level))
        self.table.setItem(idx, 3, QTableWidgetItem(task.task_status))
        self.table.setItem(idx, 4, QTableWidgetItem(task.task_description))
        self.table.setItem(idx, 5, QTableWidgetItem(task.task_hardware))
        task_comment_button = QPushButton("Commentaires")
        task_comment_button.clicked.connect(self.get_comment_button_push)
        self.table.setCellWidget(idx, 6, task_comment_button)
        task_comment_button.show()
        self.adjustSize()

    def add_new_row(self):
        # task = Task()
        # task.task_token = task.generate_token()
        # task.task_build_date = datetime.today().strftime('%d/%m/%Y')
        # idx = self.table.rowCount()
        # self.table.insertRow(idx)
        # self.table.setItem(idx, 0, QTableWidgetItem(task.task_build_date))
        # pb_task_comment = QPushButton('Commentaires')
        # self.table.setCellWidget(idx, 6, pb_task_comment)
        # self.adjustSize()
        NewTaskWindow()

    def show_win(self):
        self.show()
    
    def get_comment_button_push(self):
        idx = self.table.currentRow()
        task = Task.task_inst_db[idx]
        CommentWindow(task)


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
        # self.b_add_comment.clicked.connect(add_a_comment)
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
        self.win = self
        self.win.show()
        
    def task_builder(self):
        newTask = Task()
        newTask.task_token = newTask.task_token
        newTask.task_build_date = self.de_build_date.text()
        newTask.task_previs_finish_date = self.de_previs_date.text()
        newTask.task_last_mod_date = ""
        newTask.task_priority_level = self.cb_prio_level.currentText()
        newTask.task_hardware = self.t_hardware.text()
        newTask.task_status = self.cb_status.currentText()
        newTask.task_description = self.tb_description_box.toPlainText()
        self.win.close()
        add_task_to_tb(newTask)

class CommentWindow(QWidget):
    def __init__(self, task):
        global cb
        super().__init__()
        self.setWindowTitle("Commentaires")
        self.task = task
        self.table = QTableWidget(0, 3, parent=self)
        self.table.insertRow(0)
        self.table.setHorizontalHeaderLabels(['Build date', 'Comment', 'Number'])
        self.table.setAlternatingRowColors(True)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.win = self
        self.display_existing_comments()
        self.setFocusPolicy(Qt.StrongFocus)
        cb = self

    def display_existing_comments(self):
        for idx, elt in enumerate(self.task.task_comment):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(self.task.task_comment[idx].build_date))
            self.table.setItem(idx, 1, QTableWidgetItem(self.task.task_comment[idx].content))
            self.table.setItem(idx, 2, QTableWidgetItem(self.task.task_comment[idx].number))
        self.pb_add_comment = QPushButton('Add comment')
        self.pb_add_comment.clicked.connect(self.open_new_comment_window)
        self.layout.addWidget(self.pb_add_comment)
        self.setLayout(self.layout)
        self.win.show()

    def open_new_comment_window(self):
        NewCommentWindow(self.task)

    def add_comment(self, comment):
        idx = self.table.rowCount()
        comment = TaskComment()
        self.table.insertRow(idx)
        self.table.setItem(idx, 0, QTableWidgetItem(comment.build_date))
        self.table.setItem(idx, 1, QTableWidgetItem(comment.content))
        self.table.setItem(idx, 2, QTableWidgetItem(comment.number))
        self.adjustSize()
        

class NewCommentWindow(QWidget):
    def __init__(self, task):
        super().__init__()
        self.task = task
        self.setWindowTitle("Nouveau commentaire")
        self.tb_description_box = QTextEdit()
        self.tb_description_box.setAcceptRichText(True)
        self.b_validate = QPushButton("Valider")
        self.b_validate.clicked.connect(self.comment_builder)
        self.lb_build_date = QLabel("Date du commentaire")
        self.de_build_date = QLabel(datetime.today().strftime('%d/%m/%Y'))
        # self.b_add_comment.clicked.connect(add_a_comment)
        self.l_left_layout = QVBoxLayout()
        self.l_left_layout.addWidget(self.tb_description_box)
        self.l_left_layout.addWidget(self.b_validate)
        self.l_right_layout = QVBoxLayout()
        self.l_right_layout.addWidget(self.lb_build_date)
        self.l_right_layout.addWidget(self.de_build_date)
        self.l_right_layout.addStretch()
        self.l_pseudo_widget = QWidget()
        self.l_pseudo_widget.setLayout(self.l_right_layout)
        self.l_pseudo_widget.setMaximumWidth(200)
        self.l_layout = QHBoxLayout()
        self.l_layout.addLayout(self.l_left_layout)
        self.l_layout.addWidget(self.l_pseudo_widget)
        self.setLayout(self.l_layout)
        self.win = self
        self.win.show()

    def comment_builder(self):
        new_comment= TaskComment()
        new_comment.build_date = self.de_build_date.text()
        new_comment.content = self.tb_description_box.toPlainText()
        self.win.close()
        self.task.task_comment.append(new_comment)
        add_comment(self.task, new_comment)


def load_task_db():
    os.chdir('db')
    task_list = os.listdir()
    nb_task_in_db = len(os.listdir())
    for task_file in task_list:
        read_task = Task()
        task_file = open(task_file, 'r')
        task_file_content = task_file.read().split('\n')
        idx_des_end = [idx for idx, line in enumerate(task_file_content) if line == '[/des]'][0]
        try:
            read_task.task_token                = task_file_content[0]
            read_task.task_build_date           = task_file_content[1]
            read_task.task_previs_finish_date   = task_file_content[2]
            read_task.task_last_mod_date        = task_file_content[3]
            read_task.task_priority_level       = task_file_content[4]
            read_task.add_description(task_file_content[6:idx_des_end])
            read_task.task_hardware             = task_file_content[idx_des_end + 1]
            read_task.task_status               = task_file_content[idx_des_end + 2]
            read_task.add_comment(task_file_content[idx_des_end + 4:])
        except:
            continue

def save_task(task):
    # os.chdir('db')
    file = open('ozy_{}.task'.format(task.task_token), 'w')
    file.write('{}\n{}\n{}\n{}\n{}\n[des]\n{}\n[/des]\n{}\n{}'.format(
                task.task_token,             
                task.task_build_date,        
                task.task_previs_finish_date,
                task.task_last_mod_date,     
                task.task_priority_level,    
                task.task_description,       
                task.task_hardware,          
                task.task_status                       
    ))
    file.write('\n\n')

def add_task_to_tb(task):
    idx =tb.table.rowCount()
    tb.table.insertRow(idx)
    #self.setStyleSheet("background-color: red")
    tb.table.setItem(idx, 0, QTableWidgetItem(task.task_build_date))
    tb.table.setItem(idx, 1, QTableWidgetItem(task.task_previs_finish_date))
    tb.table.setItem(idx, 2, QTableWidgetItem(task.task_priority_level))
    tb.table.setItem(idx, 3, QTableWidgetItem(task.task_status))
    tb.table.setItem(idx, 4, QTableWidgetItem(task.task_description))
    tb.table.setItem(idx, 5, QTableWidgetItem(task.task_hardware))
    task_comment_button = QPushButton("Commentaires")
    task_comment_button.clicked.connect(tb.get_comment_button_push)
    tb.table.setCellWidget(idx, 6, task_comment_button)
    task_comment_button.show()
    save_task(task)
    tb.adjustSize()

def add_comment(task, comment):
    idx = cb.table.rowCount()
    cb.table.insertRow(idx)
    cb.table.setItem(idx, 0, QTableWidgetItem(comment.build_date))
    cb.table.setItem(idx, 1, QTableWidgetItem(comment.content))
    cb.table.setItem(idx, 2, QTableWidgetItem(comment.number))
    cb.adjustSize()
    file = open('ozy_{}.task'.format(task.task_token), 'a')
    file.write('[com]\n#{}\n{}\n[/com]\n'.format(comment.build_date, comment.content))

load_task_db()
app = QApplication(sys.argv)
tb = TaskBase()
tb.build()
tb.show()
tb.adjustSize()
cb = None
app.exec_()
