import pika
import ast
import time
from config import RABBITMQ_LOGIN, RABBITMQ_IP, RABBITMQ_PASSWORD, RABBITMQ_PORT, SERVICE_NAME
from db_writer import DatabaseLogsWriter


class Rabbit_base:
    def __init__(self, message: str = None, queue_='log_queue'):
        self.credentials = pika.PlainCredentials(username=RABBITMQ_LOGIN, password=RABBITMQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(host=RABBITMQ_IP, port=RABBITMQ_PORT, virtual_host='/',
                                                    credentials=self.credentials)
        self.connection = None
        self.channel = None
        self.message = message
        self.queue = queue_

    def connect(self):
        try:
            if not self.connection or self.connection.is_closed:
                self.connection = pika.BlockingConnection(self.parameters)
                self.channel = self.connection.channel()
                if self.connection:
                    return self.connection

        except pika.exceptions.AMQPConnectionError as error:
            time.sleep(3)
            self.connect()

        except pika.exceptions.ConnectionClosedByBroker as error:
            time.sleep(3)
            self.connect()

        except pika.exceptions.ConnectionWrongStateError as error:
            time.sleep(3)
            self.connect()


class Rabbit_listener(Rabbit_base):
    @staticmethod
    def pr(ch, method, properties, data):
        try:
            str_data = data.decode('utf-8')
            data = ast.literal_eval(str_data)
            DatabaseLogsWriter(data['service-name'], data['message'], data['datetime'], data['level_event'], data['more_information']).log_write()
        except KeyError:
            print('Отправленные данные не валидны!')

    def get_message(self):
        try:
            self.connect()
            self.channel.basic_consume(queue=self.queue,
                                       auto_ack=True,
                                       on_message_callback=self.pr)
            self.channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as error:
            time.sleep(3)
            self.connect()

        except pika.exceptions.ConnectionClosedByBroker as error:
            time.sleep(3)
            self.connect()

        except pika.exceptions.ConnectionWrongStateError as error:
            time.sleep(3)
            self.connect()


if __name__ == '__main__':
    Rabbit_listener(queue_='log_queue').get_message()
