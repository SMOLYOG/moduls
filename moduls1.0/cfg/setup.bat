@echo off
setlocal enabledelayedexpansion

set CONFIG_FILE=config.txt

if not exist "%CONFIG_FILE%" (
    echo DISCORD_TOKEN= > "%CONFIG_FILE%"
    echo DISCORD_CHANNEL_ID= >> "%CONFIG_FILE%"
    echo WEBHOOK_URL= >> "%CONFIG_FILE%"
    echo OUTPUT_MODE=bot >> "%CONFIG_FILE%"
)

for /f "usebackq tokens=1,* delims==" %%A in ("%CONFIG_FILE%") do (
    set %%A=%%B
)

echo ============================
echo Current configuration:
echo DISCORD_TOKEN=%DISCORD_TOKEN%
echo DISCORD_CHANNEL_ID=%DISCORD_CHANNEL_ID%
echo WEBHOOK_URL=%WEBHOOK_URL%
echo OUTPUT_MODE=%OUTPUT_MODE%
echo ============================

set /p NEW_TOKEN=Enter new Discord Token (leave blank to keep current): 
set /p NEW_CHANNEL=Enter new Channel ID (leave blank to keep current): 
set /p NEW_WEBHOOK=Enter new Webhook URL (leave blank to keep current): 
set /p NEW_MODE=Enter output mode (bot/webhook, leave blank to keep current): 

if not "%NEW_TOKEN%"=="" set DISCORD_TOKEN=%NEW_TOKEN%
if not "%NEW_CHANNEL%"=="" set DISCORD_CHANNEL_ID=%NEW_CHANNEL%
if not "%NEW_WEBHOOK%"=="" set WEBHOOK_URL=%NEW_WEBHOOK%
if not "%NEW_MODE%"=="" set OUTPUT_MODE=%NEW_MODE%

(
    echo DISCORD_TOKEN=%DISCORD_TOKEN%
    echo DISCORD_CHANNEL_ID=%DISCORD_CHANNEL_ID%
    echo WEBHOOK_URL=%WEBHOOK_URL%
    echo OUTPUT_MODE=%OUTPUT_MODE%
) > "%CONFIG_FILE%"

echo ============================
echo Updated configuration saved.
echo ============================
pause
endlocal
