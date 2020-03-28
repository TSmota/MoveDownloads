import os
import shutil
from win10toast import ToastNotifier
from watchdog.events import FileSystemEventHandler


class DownloadHandler(FileSystemEventHandler):
    def __init__(self, item, destination):
        self.folder = item["folder"]
        self.moveFolders = item["moveFolders"]
        self.destination_folder = destination
        self.i = 0
        self.running = False
        self.notifier = ToastNotifier()

    def map_extension(self, ext):
        word_exts = [".docx", ".doc"]
        ppt_exts = [".pptx", ".ppt"]
        music_exts = [".mp3", ".iff", ".mpa", ".wav", ".m4a"]
        exe_and_installers = [".exe", ".msi", ".jar", ".bat"]
        photos = [".jpg", ".jpeg", ".png"]
        videos = [".mp4", ".mkv", ".m4p", ".avi", ".wmv"]
        code = [".c", ".java", ".class", ".cpp", ".cs", ".h", ".lua", ".m", ".py",
                ".sh", ".swift", ".vb", ".vcxproj", ".sql", ".ts", ".tsx", ".jsx"]
        fonts = [".otf", ".woff", ".woff2", ".ttf"]

        if ext == ".pdf":
            return "PDF_DOCS"
        elif ext in word_exts:
            return "WORDS_DOCS"
        elif ext in ppt_exts:
            return "PPTX_DOCS"
        elif ext in music_exts:
            return "MUSICAS"
        elif ext in exe_and_installers:
            return "EXECUTAVEIS"
        elif ext in photos:
            return "FOTOS"
        elif ext in videos:
            return "VIDEOS"
        elif ext in code:
            return "DEV_CODES"
        elif ext == ".txt":
            return "TEXTOS"
        elif ext == ".gif":
            return "GIFS"
        elif ext in fonts:
            return "FONTS"
        else:
            return ""

    def on_modified(self, event):
        if self.running:
            return
        self.running = True
        for filename in os.listdir(self.folder):
            self.i = 0
            base_name, extension = os.path.splitext(filename)

            if extension and self.map_extension(extension.lower()) != "":
                sub_folder = self.map_extension(extension.lower()) + "/"
                if not os.path.exists(self.destination_folder + "/" + sub_folder):
                    os.mkdir(self.destination_folder + "/" + sub_folder)
                new_name = sub_folder + filename
                file_exists = os.path.isfile(
                    self.destination_folder + "/" + new_name)
                while file_exists:
                    self.i += 1
                    new_name = "{} ({}){}".format(
                        sub_folder + base_name, self.i, extension)
                    file_exists = os.path.isfile(
                        "{}/{}".format(self.destination_folder, new_name))
                source = self.folder + "/" + filename
                new_destination = self.destination_folder + "/" + new_name
                self.notifier.show_toast("Python", "Movendo arquivo {} para {}".format(
                    filename, self.destination_folder + '/' + sub_folder), duration=8)
                shutil.move(source, new_destination)
            elif not extension and self.moveFolders:  # folders
                new_destination = self.destination_folder + "/Folders/" + filename
                folder_exists = os.path.exists(new_destination)
                while folder_exists:
                    self.i += 1
                    new_name = "{} ({})".format(filename, self.i)
                    new_destination = self.destination_folder + "/Folders/" + new_name
                    folder_exists = os.path.exists(new_destination)
                source = self.folder + "/" + filename
                self.notifier.show_toast("Python", "Movendo pasta {} para {}".format(
                    filename, self.destination_folder + '/Folders'), duration=8)
                shutil.move(source, new_destination)
        self.running = False
