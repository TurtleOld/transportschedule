import asyncio
import os
from dotenv import load_dotenv
from aiohttp import web
from telebot import types

from transportschedule.schedule.telegram.config import bot, logger

load_dotenv()

API_TOKEN = os.getenv('TOKEN_TELEGRAM_BOT')
WEBHOOK_LISTEN = '31.129.104.84'
WEBHOOK_HOST = 'wh.hlvm.ru'
WEBHOOK_PORT = 443

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)


async def webhooks_handler(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = types.Update.de_json(request_body_dict)
        asyncio.ensure_future(bot.process_new_updates([update]))
        return web.Response()
    else:
        return web.Response(status=403)


async def shutdown(app):
    logger.info('Shutting down: removing webhook')
    await bot.remove_webhook()
    logger.info('Shutting down: closing session')
    await bot.close_session()


async def setup():
    # Remove webhook, it fails sometimes the set if there is a previous webhook
    logger.info('Starting up: removing old webhook')
    await bot.remove_webhook()
    # Set webhook
    logger.info('Starting up: setting webhook')
    await bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    app = web.Application()
    app.router.add_post('/{token}/', webhooks_handler)
    app.on_cleanup.append(shutdown)
    return app
