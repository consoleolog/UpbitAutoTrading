import os

from dotenv import load_dotenv


class AppProperties:
    def __init__(self):
        load_dotenv()
        self.upbit_access_key = os.getenv('UPBIT_OPEN_API_ACCESS_KEY')
        self.upbit_secret_key = os.getenv('UPBIT_OPEN_API_SECRET_KEY')
