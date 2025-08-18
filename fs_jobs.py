import os
from os import path, mkdir, remove

class fileJobs:
    def __init__(self):
        self.buttonCount = 8
        # Çalışma klasörünün altına devicefolder/pdf/
        self.baseLocation = path.join(os.getcwd(), "devicefolder")
        self.fileLocation = path.join(self.baseLocation, "pdf")
        print(f"[FILE CONTROLLER] Base location: {self.baseLocation}")
        print(f"[FILE CONTROLLER] PDF location: {self.fileLocation}")

        # Kurulum sırasında klasörleri otomatik oluştur
        self.generateFolders()

    def generateFolders(self):
        # devicefolder ve pdf klasörlerini oluştur
        if not path.isdir(self.fileLocation):
            os.makedirs(self.fileLocation)
            print(f"Ana klasör(ler) oluşturuldu: {self.fileLocation}")
        else:
            print("Ana klasör zaten var.")

        # buttonCount kadar alt klasör oluştur
        for i in range(1, self.buttonCount + 1):
            folder_path = path.join(self.fileLocation, str(i))
            if not path.isdir(folder_path):
                mkdir(folder_path)
                print(f"Klasör oluşturuldu: {folder_path}")
            else:
                print(f"Klasör zaten var: {folder_path}")

# Test
if __name__ == "__main__":
    controller = fileJobs()
