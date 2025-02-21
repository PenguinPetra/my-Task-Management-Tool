from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLabel, QDialog, QFormLayout, QLineEdit, QDateEdit, QComboBox, QCalendarWidget, QTextBrowser
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QTextCharFormat, QColor
from task_manager import TaskManager

class TaskDialog(QDialog):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setWindowTitle("タスク作成")
    self.setModal(True)

    layout = QFormLayout()
    self.task_name_input = QLineEdit()
    self.deadline_input = QDateEdit()
    self.deadline_input.setCalendarPopup(True)
    self.deadline_input.setDate(QDate.currentDate())

    self.difficulty_input = QComboBox()
    self.difficulty_input.addItems(["1", "2", "3"])

    layout.addRow("タスク名:", self.task_name_input)
    layout.addRow("提出期限:", self.deadline_input)
    layout.addRow("難易度:", self.difficulty_input)

    self.submit_button = QPushButton("作成")
    self.submit_button.clicked.connect(self.accept)
    layout.addWidget(self.submit_button)

    self.setLayout(layout)

  def get_task_data(self):
    return {
        "title": self.task_name_input.text(),
        "deadline": self.deadline_input.date().toString("yyyy-MM-dd"),
        "difficulty": int(self.difficulty_input.currentText())
    }

class TaskManagerUI(QWidget):
  def __init__(self):
    super().__init__()

    self.task_manager = TaskManager()
    self.setWindowTitle("タスク管理アプリ")
    self.setGeometry(100, 100, 500, 600)

    self.layout = QVBoxLayout()

    self.label = QLabel("タスク一覧")
    self.task_list = QListWidget()
    self.create_task_button = QPushButton("タスク作成")
    self.delete_task_button = QPushButton("タスクを削除")
    self.show_calendar_button = QPushButton("カレンダー一覧")

    self.layout.addWidget(self.label)
    self.layout.addWidget(self.task_list)
    self.layout.addWidget(self.create_task_button)
    self.layout.addWidget(self.delete_task_button)
    self.layout.addWidget(self.show_calendar_button)

    self.setLayout(self.layout)

    self.load_tasks()

    self.create_task_button.clicked.connect(self.create_task)
    self.delete_task_button.clicked.connect(self.delete_task)
    self.show_calendar_button.clicked.connect(self.show_calendar)

  def load_tasks(self):
    """タスク一覧を読み込む"""
    self.task_list.clear()
    tasks = self.task_manager.get_tasks()
    today = QDate.currentDate()

    for task in tasks:
      deadline = QDate.fromString(task['deadline'], "yyyy-MM-dd")
      days_until_deadline = today.daysTo(deadline)

      # 難易度ごとの警告日数
      warning_days = {1: 3, 2: 7, 3: 14}
      difficulty = task['difficulty']

      item_text = f"{task['title']} - 期限: {task['deadline']} - 難易度: {difficulty}"
      item = QListWidgetItem(item_text)

      if days_until_deadline <= warning_days.get(difficulty, 0):
        item.setForeground(QColor("red"))

      self.task_list.addItem(item)

  def create_task(self):
    """タスク作成ダイアログを開き、入力を取得"""
    dialog = TaskDialog(self)
    if dialog.exec() == QDialog.Accepted:
      task_data = dialog.get_task_data()
      self.task_manager.add_task(
          task_data["title"], task_data["deadline"], task_data["difficulty"])
      self.load_tasks()

  def delete_task(self):
    """選択したタスクを削除"""
    selected_item = self.task_list.currentItem()
    if selected_item:
      task_title = selected_item.text().split(" - ")[0]
      self.task_manager.delete_task(task_title)
      self.load_tasks()

  def show_calendar(self):
    """カレンダーを表示"""
    self.calendar_window = CalendarView(self.task_manager)
    self.calendar_window.show()

class CalendarView(QWidget):
  def __init__(self, task_manager):
    super().__init__()
    self.setWindowTitle("カレンダー一覧")
    self.setGeometry(200, 200, 400, 400)

    self.layout = QVBoxLayout()
    self.calendar = QCalendarWidget()
    self.task_display = QTextBrowser()
    self.layout.addWidget(self.calendar)
    self.layout.addWidget(self.task_display)

    self.setLayout(self.layout)
    self.task_manager = task_manager
    self.highlight_tasks()
    self.calendar.selectionChanged.connect(self.update_task_display)

  def highlight_tasks(self):
    """タスクのある日付に印を付ける"""
    tasks = self.task_manager.get_tasks()
    task_dates = {task["deadline"]: [] for task in tasks}
    for task in tasks:
      task_dates[task["deadline"]].append(task["title"])

    for date, titles in task_dates.items():
      qdate = QDate.fromString(date, "yyyy-MM-dd")
      format = QTextCharFormat()
      format.setBackground(QColor("lightblue"))
      self.calendar.setDateTextFormat(qdate, format)

  def update_task_display(self):
    """選択した日に対応するタスクを表示"""
    selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
    tasks = self.task_manager.get_tasks()
    task_names = [task["title"]
                  for task in tasks if task["deadline"] == selected_date]
    self.task_display.setText(
        "\n".join(task_names) if task_names else "タスクなし")
