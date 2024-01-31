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
