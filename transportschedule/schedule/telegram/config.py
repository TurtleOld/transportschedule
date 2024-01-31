"""Settings telegram bot."""

import logging
import os

import telebot
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

load_dotenv()
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
token = os.getenv('TOKEN_TELEGRAM_BOT')
bot = AsyncTeleBot(token, parse_mode='html')


WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PORT = os.getenv('WEBHOOK_PORT')
WEBHOOK_LISTEN = os.getenv('WEBHOOK_LISTEN')
WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(token)
