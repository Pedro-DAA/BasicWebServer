from socket import *
from multiprocessing import *

#insert the file path where your file are located under here
FILELOCATION = ""

class commAndFile: 
    command = ""
    file = ""

def readNext(data):
    reading = commAndFile()
    curComm = ""
    for line in data:
        if (line == " "):
            if reading.command == "":
                reading.command = curComm
                curComm = ""
            else: 
                reading.file = curComm
                break
        else:
            curComm = curComm + line
    return reading

def get(file,client):
    filePath = ""
    try:
        if file == "/":
            filePath = FILELOCATION + "INSERT MAIN.html file name here"
        else:
            filePath = FILELOCATION + file
        curRequest = open(filePath, "rb")
        line = curRequest.read(1024)
        while (line):
            client.send(line)
            line = curRequest.read(1024)
        return 0

    except:
        raise Exception("file not found")
        return 1




def worker(client):
    while(True):
        data = client.recv(2048)
        data = data.decode()
        curJob = commAndFile()
        curJob = readNext(data)
        print(curJob.command)
        match curJob.command:
            case "GET":
                get(curJob.file,client)
        break

    return 0

def server():

    serverSocket = socket(AF_INET, SOCK_STREAM)
    print(gethostname())
    #insert IP address under here
    serverSocket.bind(('', 80))
    serverSocket.listen(5)
    try:
        while True:
            (clientSocket, address) = serverSocket.accept()
            worker(clientSocket)
            
            clientSocket.shutdown(SHUT_RDWR)
            clientSocket.close()
    except KeyboardInterrupt:
        serverSocket.shutdown(SHUT_RDWR)    
        serverSocket.close()

server()


