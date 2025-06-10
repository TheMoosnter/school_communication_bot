from .db import get_connection


class StudentsDB:
    def add(self,
        tg_id: int,
        username: str,
        first_name: str,
        last_name: str,
        class_number: int,
        class_letter: str,
        is_registered: bool,
    ):
        """
        Добавляет ученика в таблицу students.
        :param tg_id: айди телеграмм-аккаунта ученика
        :param username: никнейм телеграмм-аккаунта
        :param first_name: имя ученика
        :param last_name: фамилия ученика
        :param class_number: номер класса
        :param class_letter: буква класса
        :param is_registered: прошёл ли ученик регистрацию
        :return:
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO students (telegram_id, username, first_name, last_name, class_number, class_letter, is_registered)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    tg_id,
                    username,
                    first_name,
                    last_name,
                    class_number,
                    class_letter,
                    is_registered,
                ),
            )
            conn.commit()


    def remove(self, tg_id: int):
        """
        Удаляет аккаунт из базы данных
        :param tg_id: айди телеграмм-аккаунта
        :return: если аккаунт отсутствует в базе данных, возвращает функцию
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM students WHERE telegram_id = ?", (tg_id,))
            if cursor.fetchone() is None:
                return

            cursor.execute("DELETE FROM students WHERE telegram_id=?", (tg_id,))
            conn.commit()


    def print(self):
        """
        Возвращает список учеников из базы данных.
        :return: список кортежей с данными учеников
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            return cursor.fetchall()


    def exists(self, tg_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM students WHERE telegram_id=?", (tg_id,))
            return cursor.fetchone() is not None


    def is_registered(self, tg_id: int):
        """
        Проверяет наличие телеграмм-акаунта в базе данных.
        :param tg_id: айди телеграмм акаунта
        :return: true, если аккаунт уже есть в БД, false, если отсутствует.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM students WHERE telegram_id=? AND is_registered=1", (tg_id,)
            )
            return cursor.fetchone() is not None


    def register(self, tg_id: int):
        """
        Завершает процесс регистрации ученика.
        :param tg_id: телеграмм-аккаунт ученика
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET is_registered = 1 WHERE telegram_id = ?", (tg_id,)
            )
            conn.commit()


    def get_name(self, tg_id: int):
        """
        Возвращает имя ученика по айди телеграмм-аккаунта
        :param tg_id: айди телеграмм акаунта
        :return: имя ученика
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT first_name FROM students WHERE telegram_id=?", (tg_id,))
            return cursor.fetchone()[0]


    def get_surname(self, tg_id: int):
        """
        Возвращает фамилию ученика по айди телеграмм-аккаунта
        :param tg_id: айди телеграмм акаунта
        :return: фамилия ученика
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT last_name FROM students WHERE telegram_id=?", (tg_id,))
            return cursor.fetchone()[0]


    def get_class_number(self, tg_id: int):
        """
        Возвращает номер класса ученика по айди телеграмм-аккаунта
        :param tg_id: айди телеграмм акаунта
        :return: фамилия ученика
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT class_number FROM students WHERE telegram_id=?", (tg_id,))
            return cursor.fetchone()[0]


    def get_class_letter(self, tg_id: int):
        """
        Возвращает букву класса ученика по айди телеграмм-аккаунта
        :param tg_id: айди телеграмм акаунта
        :return: фамилия ученика
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT class_letter FROM students WHERE telegram_id=?", (tg_id,))
            return cursor.fetchone()[0]
