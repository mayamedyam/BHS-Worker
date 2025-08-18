import os
from os import path, mkdir, listdir, remove

class fileJobs:
    def __init__(self):
        self.buttonCount = 8
        self.fileLocation = f"{os.getcwd()}/pdf/"
        print(f"[FILE CONTROLLER | MAIN] Completed successfully")
        
        # Kurulum sırasında PDF klasörlerini otomatik oluştur
        self.generateFolders()

    def generateFolders(self):
        for file in range(self.buttonCount):
            file += 1
            folder_path = self.fileLocation + str(file)
            if not path.isdir(folder_path):
                mkdir(folder_path)
                print(f"Klasör oluşturuldu: {folder_path}")

    def getFiles(self, folder: int) -> list:
        pathway = self.fileLocation + str(folder) + "/"
        return [os.path.splitext(filename)[0] for filename in os.listdir(pathway)]

    def saveFile(self, button: int, fileName: str, content):
        pathway = self.fileLocation + str(button) + "/"
        file = open(pathway + fileName + ".pdf", "wb")
        file.write(content)
        file.close()

    def deleteFiles(self, button: int, files: list):
        for file in files:
            pathway = self.fileLocation + str(button) + "/" + file + '.pdf'
            if path.exists(pathway):
                remove(pathway)
