import psutil, time

def get_system_status():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "time": int(time.time())
    }
