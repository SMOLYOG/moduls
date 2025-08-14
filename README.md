# 🖥️ Discord System Info Reporter

A Python-based tool for sending **detailed system, network, and screenshot information** to a Discord channel, either via **Bot** or **Webhook**.

## ✨ Features
- Public IP & ISP information (with location from IP-API)
- Local IPv4 addresses
- CPU model (e.g., `AMD Ryzen 5 3600`, `Intel i5-11400`)
- GPU detection (NVIDIA, AMD, Intel)
- RAM & disk usage
- Windows license key extraction
- Current logged-in username
- **Automatic screenshot capture** and upload to Discord
- Sends output to Discord:
  - via **Bot** (using Discord API)
  - via **Webhook** (no bot account required)
- Centralized configuration file (`config.cfg`)
- Works regardless of where the script is run from

---

## ⚙️ Configuration

The `config.txt` file controls all settings:

```ini
DISCORD_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=123456789012345678
WEBHOOK_URL=https://discord.com/api/webhooks/xxxxx/yyyyy
OUTPUT_MODE=bot
```

**Fields:**
- `DISCORD_TOKEN` → Your bot's token (only used if `OUTPUT_MODE=bot`)
- `DISCORD_CHANNEL_ID` → Channel ID for bot messages
- `WEBHOOK_URL` → Webhook URL (only used if `OUTPUT_MODE=webhook`)
- `OUTPUT_MODE` → Choose `bot` or `webhook`

You can quickly edit the config by running:
```bat
setup.bat
```

---

## 🚀 Installation & Usage

### 1️⃣ Install dependencies
run install.bat 

### 2️⃣ Setup configuration
run 'setup.bat' with your bot token or webhook.

### 3️⃣ Run the script
```bash
python info_bot.py or ss.py for screenshot
```

---

## 📸 Screenshot Feature
This script will:
1. Take a full screenshot of the desktop using **Pillow**.
2. Save it temporarily.
3. Send it as an image file to your selected Discord channel or webhook.
4. Automatically delete the temporary file after sending.

---

## 📌 Example Output (in Discord)
```
System & Network Report (local machine)
👤 Username: user123
🔑 Windows License Key: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
🌐 Public IP: 72.14.201.46
📍 Location: New York, NY, United States
📌 Coordinates: 40.7128, -74.0060
🏢 ISP: Verizon
💻 Local IPv4: 192.168.1.10
🖥 System: Windows-10-10.0.19045-SP0
⚙ CPU: AMD Ryzen 5 3600
💾 RAM: 16 GB
💽 Disk: 512 GB
🎮 GPU: NVIDIA GeForce GTX 1660 Ti
📷 Screenshot: [Attached Image]
```

---

## 🛡 Disclaimer
This tool is intended for **educational and authorized use only**.  
Do not run it on machines you do not own or have explicit permission to test.

