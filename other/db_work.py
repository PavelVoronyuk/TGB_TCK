import sqlite3

class DBwork:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def check_user(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def check_docs(self, user_id):
        result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return len(result) > 2


    def reg_docs(self, user_id, name, surname, birth, fought, goden, judged):
        with self.connection:
            self.cursor.execute("""UPDATE `users`
            SET `name` = ?, `surname` = ?, `birth` = ?, `fought` = ?, `goden` = ?, `judged` = ?
            WHERE `user_id` = ?""", (name, surname, birth, fought, goden, judged, user_id,))

    def get_docs(self, user_id):
        with self.connection:
            result = self.cursor.execute("""SELECT `name`, `surname`, `birth`, `fought`, `goden`, `judged` FROM `users` WHERE `user_id` = ?""", (user_id,)).fetchone()
            lst = list(result)
            return f"""Вот ваши документы:
Имя: {lst[0]}
Фамилия: {lst[1]}
Возраст: {lst[2]}
Служил: {lst[3]}
Годен: {lst[4]}
Судимость: {lst[5]}"""