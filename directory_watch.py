from supabase import create_client
from dotenv import  load_dotenv
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)
class Watcher:
    def __init__(self, directories_to_watch):
        self.directories_to_watch = directories_to_watch
        self.event_handler = Handler()
        self.observer = Observer()

    def run(self):
        for directory in self.directories_to_watch:
            self.observer.schedule(self.event_handler, directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        try:
            print(f"Created: {event.src_path}")
            supabase.table("directory").insert({"operation":'created', "path": f'{event.src_path}'}).execute()
        except Exception as e:
            print(f"Error inserting data: {e}")

    @staticmethod
    def on_deleted(event):
        try:
            print(f"Deleted: {event.src_path}")
            supabase.table("directory").insert({"operation": 'deleted', "path": f'{event.src_path}'}).execute()
        except Exception as e:
            print(f"Error inserting data: {e}")

    @staticmethod
    def on_modified(event):
        try:
            print(f"Modified: {event.src_path}")
            supabase.table("directory").insert({"operation": 'modified', "path": f'{event.src_path}'}).execute()
        except Exception as e:
            print(f"Error inserting data: {e}")

    @staticmethod
    def on_moved(event):
        try:
            print(f"Moved: from {event.src_path} to {event.dest_path}")
            supabase.table("directory").insert({"operation": 'moved', "path": f'{event.src_path}'}).execute()
        except Exception as e:
            print(f"Error inserting data: {e}")

if __name__ == "__main__":
    directories_to_watch = [
        "./",   # Change this to your first directory
        r"C:\Users\samru\Desktop\Basic_Network_Scanner",  # Change this to your second directory
        # Add more directories as needed
    ]
    w = Watcher(directories_to_watch)
    w.run()
