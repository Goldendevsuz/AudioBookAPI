import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class RestartOnChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        print("Starting Celery worker...")
        self.process = subprocess.Popen(self.command, shell=True)

    def stop_process(self):
        if self.process:
            print("Stopping Celery worker...")
            self.process.terminate()
            self.process.wait()

    def on_any_event(self, event):
        self.stop_process()
        self.start_process()


if __name__ == "__main__":
    command = "celery -A AudioBook worker --loglevel=info"
    event_handler = RestartOnChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)

    print("Watching for file changes...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        event_handler.stop_process()

    observer.join()
