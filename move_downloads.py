import os
import time

from watchdog.observers import Observer
from win10toast import ToastNotifier

from folders import folders_to_track
from download_handler import DownloadHandler

def main():
    ToastNotifier().show_toast("Python - Mover arquivos em downloads", "Script para mover arquivos da pasta de download do SSD para HD iniciado")

    folder_destination = "D:/Downloads"
    observer = Observer()

    for item in folders_to_track:
        event_handler = DownloadHandler(item, folder_destination)
        observer.schedule(event_handler, item["folder"], recursive=True)
        
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()