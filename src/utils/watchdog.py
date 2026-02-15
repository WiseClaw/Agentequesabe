import sys, os
sys.path.append(os.getcwd())

import subprocess
import time
import os

services = [
    {"name": "Discord Bot", "cmd": ["python", "src/interfaces/discord_bot.py"]},
    {"name": "Telegram Bot", "cmd": ["python", "src/interfaces/telegram_bot.py"]},
    {"name": "Dashboard", "cmd": ["streamlit", "run", "src/dashboard/app.py", "--server.port", "8501"]},
    {"name": "Sentinel Loop", "cmd": ["python", "src/utils/sentinel_loop.py"]}
]

def start_services():
    processes = []
    for service in services:
        print(f"🚀 Iniciando {service['name']}...")
        p = subprocess.Popen(service['cmd'])
        processes.append((service, p))
    return processes

if __name__ == '__main__':
    print("🛡️ WiseClaw Watchdog v5.0 Ativo")
    procs = start_services()
    while True:
        for i, (service, p) in enumerate(procs):
            if p.poll() is not None:
                print(f"⚠️ {service['name']} parou. Reiniciando...")
                procs[i] = (service, subprocess.Popen(service['cmd']))
        time.sleep(30)
