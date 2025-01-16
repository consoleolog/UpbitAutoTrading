import os
import unittest

from dotenv import load_dotenv
from slack_sdk import WebClient


class SlackTest(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.slack_token = os.getenv('SLACK_TOKEN')

    def test_test(self):
        client = WebClient(token=self.slack_token)
        response = client.chat_postMessage(channel='#public-bot', text="MORE!")
        print(response)