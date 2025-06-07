from .db import get_connection

def create_student_table():
    """
    Создаёт таблицу students (если её не существует)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                class_number INTEGER NOT NULL,
                class_letter TEXT NOT NULL,
                is_registered BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)
        conn.commit()