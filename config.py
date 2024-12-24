import os

from dotenv import load_dotenv


class AppProperties:
    load_dotenv()
    def __init__(self):
        self.upbit_access_key = os.getenv('UPBIT_OPEN_API_ACCESS_KEY')
        self.upbit_secret_key = os.getenv('UPBIT_OPEN_API_SECRET_KEY')

        self.smtp_from = os.getenv('SMTP_FROM')
        self.smtp_to = os.getenv('SMTP_TO')
        self.smtp_host = os.getenv('SMTP_HOST')
        self.smtp_port = os.getenv('SMTP_PORT')
        self.smtp_id = os.getenv('SMTP_ID')
        self.smtp_password = os.getenv('SMTP_PASSWORD')

        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PWD')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_name = os.getenv('DB_NAME')
