import asyncio
from transportschedule.schedule.telegram.commands import start_bot


def main():
    """Engine."""
    asyncio.run(start_bot())


if __name__ == '__main__':
    main()
