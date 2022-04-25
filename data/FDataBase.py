import sqlite3

from Lab3.task3.data.users import User


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM urls'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Дерьмо с подключением БД")
        return []

    def getAllUsers(self):
        try:
            self.__cur.execute(f"SELECT * FROM users")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения пользователя из БД " + str(e))
        return []

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД' + str(e))

        return False

    def GetUserByEmail(self, user_email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{user_email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print('User not found')
                return False
            return res
        except sqlite3.Error as e:
            print("Error getting data " + str(e))

        return False

    def updateUser(self, id, name, email, age):
        try:
            print(id, name, age, email)
            self.__cur.execute(
                f"UPDATE users SET name = '{name}', email='{email}', age='{age}'  WHERE id = '{id}'")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения пользователя из БД " + str(e))
        # return(False)
