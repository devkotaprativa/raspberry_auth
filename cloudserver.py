import io
from socket import *
serverPort=6000
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(5)
print('server ready to receive')
while 1:
    connectionSocket,addr=serverSocket.accept()
    print('Reading the image')
    with open('image.jpg','rb') as testimg:
        jpgdata=testimg.read()
        connectionSocket.send(jpgdata)
    testimg.close()
    print("Image sent")
    connectionSocket.close()
    connectionSocket,addr=serverSocket.accept()
    print("Authentication Status")
    with open('authstatus.txt','w') as status:
        inputdata=connectionSocket.recv(100)
        print inputdata
        if(inputdata=="1"):
            status.write("Authentication Successfull")
        else:
            status.write("Authentication Failed:")
