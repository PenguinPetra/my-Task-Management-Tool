import sqlite3

class Storage:
  def __init__(self):
    self.conn = sqlite3.connect("tasks.db")
    self.cursor = self.conn.cursor()
    self.create_table()

  def create_table(self):
    """タスク管理用のテーブルを作成"""
    self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                deadline TEXT,
                                difficulty INTEGER)''')
    self.conn.commit()

  def save_task(self, task):
    """タスクをデータベースに保存"""
    self.cursor.execute("INSERT INTO tasks (title, deadline, difficulty) VALUES (?, ?, ?)",
                        (task["title"], task["deadline"], task["difficulty"]))
    self.conn.commit()

  def remove_task(self, title):
    """タスクを削除"""
    self.cursor.execute("DELETE FROM tasks WHERE title = ?", (title,))
    self.conn.commit()

  def load_tasks(self):
    """すべてのタスクを取得"""
    self.cursor.execute("SELECT title, deadline, difficulty FROM tasks")
    rows = self.cursor.fetchall()
    tasks = [{"title": row[0], "deadline": row[1], "difficulty": row[2]}
             for row in rows]
    return tasks
