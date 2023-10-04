import psycopg2
from config import *
import datetime


class Database:
    def __init__(self):
        self.__user = username
        self.__password = password
        self.__port = port
        self.__host = host
        self.__database = db_name

    def connection(self):
        try:
            self.connection_creds = psycopg2.connect(database=self.__database, host=self.__host,
                                               port=self.__port, user=self.__user, password=self.__password)
            self.__cur = self.connection_creds.cursor()
            return self.__cur
        except Exception as exc:
            print(f'Ошибка: {exc}')

    def close_connection(self):
        try:
            self.__cur.close()
            self.connection_creds.close()
        except Exception as exc:
            print(f'Ошибка: {exc}')


class DatabaseLogsWriter(Database):
    def __init__(self, name_service, message, date_time, level_event, more_information):
        super().__init__()
        self.name_service = name_service
        self.message = message
        self.date_time = date_time
        self.level_event = level_event
        self.more_information = more_information

    def log_write(self):
        self.cur = self.connection()
        write_user = "insert into main_backend_logs (name_service, message, date_time, level_event, more_information) values (%s, %s, %s, %s, %s)"
        self.date_time = datetime.datetime.strptime(self.date_time, '%Y-%m-%d %H:%M:%S,%f')
        self.cur.execute(write_user, (self.name_service, self.message, self.date_time, self.level_event, self.more_information))
        self.cur.connection.commit()
        self.close_connection()
