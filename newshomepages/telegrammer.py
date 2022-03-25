import os
import time
from datetime import datetime
from pathlib import Path

import click
import pytz
from telegram import Bot

from . import utils

TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")


@click.group()
def cli():
    """Send a Telegram message."""
    pass


@cli.command()
@click.argument("handle")
@click.option("-i", "--input-dir", "input_dir", default="./")
def single(handle: str, input_dir: str):
    """Send a single source."""
    input_path = Path(input_dir)
    _post(handle, input_path)


@cli.command()
@click.argument("slug")
@click.option("-i", "--input-dir", "input_dir", default="./")
def bundle(slug: str, input_dir: str):
    """Send a bundle of sources."""
    bundle = utils.get_bundle(slug)
    handle_list = [
        h["handle"] for h in utils.get_site_list() if h["bundle"] == bundle["slug"]
    ]
    input_path = Path(input_dir)
    for handle in handle_list:
        _post(handle, input_path)
        time.sleep(2.5)


def _post(handle: str, input_dir: Path):
    # Pull the source’s metadata
    data = utils.get_site(handle)

    # Connect to Telegram
    assert isinstance(TELEGRAM_API_KEY, str)
    bot = Bot(token=TELEGRAM_API_KEY)

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(data["timezone"])
    now_local = now.astimezone(tz)

    # Create the caption
    caption = (
        f"The {data['name']} homepage at {now_local.strftime('%-I:%M %p')} local time"
    )

    # Get the image
    io = open(input_dir / f"{handle}.jpg", "rb")

    # Send the photo
    bot.sendPhoto("@newshomepages", io, caption=caption)


if __name__ == "__main__":
    cli()
