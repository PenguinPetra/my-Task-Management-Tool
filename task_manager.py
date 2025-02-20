from storage import Storage

class TaskManager:
  def __init__(self):
    self.storage = Storage()

  def add_task(self, title, deadline, difficulty):
    """タスクを追加"""
    task = {
        "title": title,
        "deadline": deadline,
        "difficulty": difficulty
    }
    self.storage.save_task(task)

  def delete_task(self, title):
    """タスクを削除"""
    self.storage.remove_task(title)

  def get_tasks(self):
    """すべてのタスクを取得"""
    return self.storage.load_tasks()
