import time
import threading

def schedule_task(task, interval_minutes=2):
    """
    Repeatedly runs the given task every X minutes in a background thread.
    """
    def run():
        while True:
            print(f"\n⏰ Running scheduled task...")
            try:
                task()
            except Exception as e:
                print(f"❌ Task failed: {e}")
            print(f"✅ Task done. Sleeping {interval_minutes} minutes...\n")
            time.sleep(interval_minutes * 60)

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
