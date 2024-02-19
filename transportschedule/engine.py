import asyncio

from aiohttp import web

from transportschedule.schedule.telegram.commands import start_bot
from transportschedule.schedule.telegram.webhooks.webhooks import (
    setup,
    WEBHOOK_LISTEN,
    WEBHOOK_PORT,
)


def main():
    """Engine."""
    web.run_app(
        setup(),
        host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
    )


if __name__ == '__main__':
    main()
