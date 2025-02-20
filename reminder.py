from datetime import datetime, timedelta
from storage import Storage

class Reminder:
  def __init__(self):
    self.storage = Storage()

  def check_deadlines(self):
    """期限が迫ったタスクを判定"""
    tasks = self.storage.load_tasks()
    today = datetime.today().date()

    for task in tasks:
      deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
      difficulty = task["difficulty"]

      # 難易度ごとの警告期間
      warning_days = {1: 3, 2: 7, 3: 14}
      warning_date = deadline - timedelta(days=warning_days[difficulty])

      if today >= warning_date:
        print(f"⚠️ タスク「{task['title']}」の期限が迫っています！")
