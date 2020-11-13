import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from diaryMain import Ui_MainWindow
from diaryTask import Ui_Dialog
from Diary import db_session
from tasks import DiaryTasks
from datetime import datetime


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


class Task(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonSave.clicked.connect(self.__save_task)

    def __save_task(self):
        t_title = self.textEditTitle.toPlainText()
        t_content = self.textEditContent.toPlainText()
        t_time = self.timeEdit.time()
        t_date_end = self.dateEdit.date()
        task_for_table = DiaryTasks()
        task_for_table.task_title = t_title
        task_for_table.task_content = t_content
        task_for_table.task_created_date = datetime.now()
        task_for_table.task_end_date = t_date_end.toPyDate()
        task_for_table.task_end_time = t_time.toPyTime()
        session.add(task_for_table)
        session.commit()
        self.close()


class Diary(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_task()
        self.chosen_date = datetime.now().date()
        self.pushButtonAdd.clicked.connect(self.__add_task)
        self.pushButtonChange.clicked.connect(self.__change_task)
        self.pushButtonDelete.clicked.connect(self.__delete_task)
        self.pushButtonChooseDate.clicked.connect(self.__show_tasks_by_date)
        self.pushButtonDiscardDate.clicked.connect(self.init_task)

    def init_task(self):
        self.listWidget.clear()
        reader = session.query(DiaryTasks).filter_by(task_end_date=datetime.now().date())
        for instance in reader.order_by(DiaryTasks.task_end_time):
            self.listWidget.addItem(str(f'{instance.task_title}\n  {instance.task_content}\n'
                                        f'  {instance.task_end_date.strftime("%Y-%m-%d")}\n'
                                        f'  {instance.task_end_time.strftime("%H:%M")}'))

    def __show_tasks_by_date(self):
        self.listWidget.clear()
        date_from_calendar = self.calendarWidget.selectedDate().toPyDate()
        reader = session.query(DiaryTasks).filter_by(task_end_date=date_from_calendar)
        for instance in reader.order_by(DiaryTasks.task_end_time):
            self.listWidget.addItem(str(f"{instance.task_title}\n  {instance.task_content}\n"
                                        f'  {instance.task_end_date.strftime("%Y-%m-%d")}\n'
                                        f'  {instance.task_end_time.strftime("%H:%M")}'))
        self.chosen_date = date_from_calendar

    def __add_task(self):
        example = Task()
        example.type = 'adding'
        example.dateEdit.setDate(self.chosen_date)
        example.exec()
        self.__show_tasks_by_date()

    def __change_task(self):
        reader = session.query(DiaryTasks).filter_by(task_end_date=self.chosen_date)
        row = reader.order_by(DiaryTasks.task_end_time)[self.listWidget.currentRow()]
        example = Task()
        example.type = 'changing'
        example.textEditTitle.append(row.task_title)
        example.textEditContent.append((row.task_content))
        example.dateEdit.setDate(row.task_end_date)
        example.timeEdit.setTime(row.task_end_time)
        example.exec()
        session.delete(row)
        session.commit()
        self.__show_tasks_by_date()

    def __delete_task(self):
        reader = session.query(DiaryTasks).filter_by(task_end_date=self.chosen_date)
        row = reader.order_by(DiaryTasks.task_end_time)[self.listWidget.currentRow()]
        session.delete(row)
        session.commit()
        self.__show_tasks_by_date()


sys._excepthook = sys.excepthook

sys.excepthook = exception_hook

db_session.global_init('tasks.db')
session = db_session.create_session()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Diary()
    ex.show()
    sys.exit(app.exec_())