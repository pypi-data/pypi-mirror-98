#  Copyright (c) ChernV (@otter18), 2021.

import logging
from logging import StreamHandler
from time import time, sleep
from typing import List

import telebot

# logging setup
logger = logging.getLogger(__name__)


class TgLoggerHandler(StreamHandler):
    """Logger handler for tg_logger"""

    def __init__(self, token: str, users: List[int], timeout: int = 10):
        """
        Setup TgLoggerHandler class

        :param token: tg bot token to log form
        :param users: list of used_id to log to
        :param timeout: seconds for retrying to send log if error occupied
        """

        super().__init__()
        self.token = token
        self.users = users
        self.timeout = timeout

        self.bot = telebot.TeleBot(token=self.token)

    def emit(self, record):
        msg = self.format(record)
        for user_id in self.users:
            t0 = time()
            while time() - t0 < self.timeout:
                try:
                    self.bot.send_message(user_id, msg, parse_mode="HTML")
                    break
                except Exception as ex:
                    logger.exception("Exception while sending %s to %s:", msg, user_id)
                    sleep(1)
