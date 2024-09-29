import os
import subprocess
import threading
from typing import Callable
from loguru import logger

env_file = '.env'

def commands() -> None:
    subprocess.run(['python3', '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    def celery_run() -> None:
        subprocess.run(['python3', '-m', 'celery', '-A', 'tasks.main', 'worker', '--concurrency=10', '--queues=high_priority'])
        
        return
        
    def fastapi_run() -> None:
        subprocess.run(['python3', 'main.py'])
        
        return
        
    th1 = threading.Thread(target=celery_run)
    th2 = threading.Thread(target=fastapi_run)
    for th in [th1, th2]:
        th.start()
    
    return

def load_env() -> Callable[..., None]:
    global env_file
    
    if not os.path.exists(env_file):
        logger.error('.env file not exists!')
        return
        
    with open(env_file, 'r') as file:
        data = file.readlines()
        
    if not data:
        return commands()
        
    for item in data:
        key_pair = item.split('=') if '=' in item else []
        if not key_pair:
            continue
        
        key = key_pair[0].strip()
        value = key_pair[1].replace('\n', '').strip()
        
        os.environ[key] = value
    
    return commands()
        
if __name__ == '__main__':
    load_env()
