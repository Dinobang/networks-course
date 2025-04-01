# import tkinter as tk
from ftplib import FTP
# from tkinter import messagebox

def FTPConnect(host, port, username, password):
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login(username, password)
    return ftp

def CreateFolder(ftp, foldername):
    ftp.mkd(foldername)

def DeleteFolder(ftp, foldername):
    ftp.rmd(foldername)

def GoToFolder(ftp, foldername):
    ftp.cwd(foldername)

def UploadFile(ftp, filename):
    with open(filename, 'rb') as file:
        ftp.storbinary('STOR ' + filename, file)

def DownloadFile(ftp, filename):
    with open(filename, 'wb') as file:
        ftp.retrbinary('RETR ' + filename, file.write)

def ListFiles(ftp):
    files = []
    ftp.dir(files.append)
    return files

def DeleteFile(ftp, filename):
    ftp.delete(filename)



def main():
    host = 'ftp.dlptest.com'
    port = 21
    username = 'dlpuser'
    password = 'rNrKYTX9g7z3RgJRmxWuGHbeu'

    ftp = FTPConnect(host, port, username, password)

    print(""" help
          Доступны следующие команды: 
          - ls - список файлов
          - download / get - скачать файл 
          - upload file /send - загрузить файл 
          - cd - перейти в папку
          - mkdir - создать директорию
          - rm - удаление папки 
          - remove - удаление файла """)


    while True:
        print()
        inp = input()
        command_all = inp.split()
        command = command_all[0]
        if len(command_all) > 1:
            args = inp[inp.find(' ') + 1: ]

        if command == 'exit': #выход
            break

        elif command == 'download' or command == 'get':
            filename = args
            DownloadFile(ftp, filename)
            print(f"Файл '{filename}' успешно скачан.")

        elif command == 'upload' or command == 'send':
            filename = args
            UploadFile(ftp, filename)
            print(f"Файл '{filename}' успешно загружен на сервер.")

        elif command == 'cd':
            foldername = args
            GoToFolder(ftp, foldername)

        elif command == 'mkdir':
            foldername = args
            CreateFolder(ftp, foldername)
        
        elif command == 'ls': #список файлов
            files = ListFiles(ftp)
            print('Список файлов')
            for file in files:
                print(file)
        
        elif command == 'remove':
            filename = args
            DeleteFile(ftp, filename)

        elif command == 'rm':
            foldername = args
            DeleteFolder(ftp, foldername)

        else:
            print("Команда не распознана")

    ftp.quit()
    print("Выход")

if __name__ == "__main__":
    main()