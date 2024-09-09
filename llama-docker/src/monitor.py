import psutil
import time

def log_resources():
    with open("resources.log", "a") as log:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            log.write(f"CPU: {cpu_usage}% | Memory: {memory_info.percent}%\n")
            time.sleep(60)  # Log every 60 seconds

if __name__ == "__main__":
    log_resources()
