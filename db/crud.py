from .db import get_connection

def add_students(tg_id: int, first_name: str, last_name: str, class_number: int, class_letter: str, is_registered: bool):
    """
    Добавляет ученика в таблицу students.
    :param tg_id: айди телеграмм-аккаунта ученика
    :param first_name: имя ученика
    :param last_name: фамилия ученика
    :param class_number: номер класса
    :param class_letter: буква класса
    :param is_registered: прошёл ли ученик регистрацию
    :return:
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (telegram_id, first_name, last_name, class_number, class_letter, is_registered)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tg_id, first_name, last_name, class_number, class_letter, is_registered))
        conn.commit()

def print_students():
    """
    Возвращает список учеников из базы данных.
    :return: список кортежей с данными учеников
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()
