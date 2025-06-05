from .db import get_connection

def add_students(tg_id: int, first_name: str, last_name: str, class_number: int, class_letter: str, is_registered: bool):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (telegram_id, first_name, last_name, class_number, class_letter, is_registered)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tg_id, first_name, last_name, class_number, class_letter, is_registered))
        conn.commit()

def print_students():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()
