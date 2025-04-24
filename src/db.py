
import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    amount REAL
                )
            """)
            conn.commit()

    def add_expense(self, name: str, amount: float):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO expenses (name, amount) VALUES (?, ?)
            """, (name, amount))
            conn.commit()

    def get_all_expenses(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, amount FROM expenses")
            return cursor.fetchall()

    def get_total(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM expenses")
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0