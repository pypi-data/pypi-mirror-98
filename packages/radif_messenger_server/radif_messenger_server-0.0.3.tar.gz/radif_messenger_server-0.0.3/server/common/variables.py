"""Константы"""
import os
from logging import DEBUG, ERROR

PROJECT_PATH = os.getcwd()
PLUGINS_PATH = os.path.join(
    PROJECT_PATH, "../../../venv/Lib/site-packages/PyQt5/Qt5/plugins")

CLIENT_PATH = os.path.join(PROJECT_PATH, "client")
CLIENT_FILE = os.path.join(CLIENT_PATH, "client.py")
CLIENT_KEYS_PATH = os.path.join(CLIENT_PATH, "keys")
CLIENT_DATABASES_PATH = os.path.join(CLIENT_PATH, "databases")

SERVER_PATH = os.path.join(PROJECT_PATH, "server")
SERVER_FILE = os.path.join(SERVER_PATH, "server.py")
SERVER_SETTINGS_PATH = os.path.join(PROJECT_PATH, "server.ini")

LOGS_PATH = os.path.join(PROJECT_PATH, "logs")
LOG_CONFIGS_PATH = os.path.join(LOGS_PATH, "configs")
LOG_FILES_PATH = os.path.join(LOGS_PATH, "log_files")
CLIENT_LOG_FILE = os.path.join(LOG_FILES_PATH, "client.log")
SERVER_LOG_FILE = os.path.join(LOG_FILES_PATH, "server.log")


# Порт по умолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'
# Текущий уровень логирования
LOGGING_LEVEL = DEBUG
# Текущий уровень логирования для потокового вывода
LOGGING_LEVEL_FOR_STREAM_HANDLER = ERROR
# на время отладки потоковый вывод иногда так же ставлю в DEBUG
# LOGGING_LEVEL_FOR_STREAM_HANDLER = DEBUG
# База данных для хранения данных сервера:
# SERVER_DATABASE = 'sqlite:///database.db3'
SERVER_CONFIG = 'server.ini'

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

# Словари - ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 202
RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO: None
                }
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
# 205
RESPONSE_205 = {
    RESPONSE: 205
}

# 511
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}

IMG = 'server/img'
EXIT_IMG = f'{IMG}/exit.png'
