@echo off
setlocal

powershell -WindowStyle Hidden -Command ^
"try { ^
    python --version > $null 2>&1; ^
    if ($LASTEXITCODE -ne 0) { ^
        $installer = Join-Path $env:TEMP 'python-installer.exe'; ^
        Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile $installer; ^
        Start-Process -FilePath $installer -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1 Include_pip=1' -Wait -NoNewWindow; ^
    } ^
    python -m pip install --upgrade pip --quiet; ^
    python -m pip install discord.py requests psutil py-cpuinfo Pillow --quiet; ^
} catch { exit 1 }"

exit /b
