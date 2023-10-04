import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

RABBITMQ_LOGIN = os.getenv("RABBITMQ_LOGIN")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_IP = os.getenv("RABBITMQ_IP")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
db_name = os.getenv("DB_NAME")
username = os.getenv("RABBITMQ_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
SERVICE_NAME = 'FACE RECOGNITION SERVICE'


