import socket
from PIL import Image
import receiveScreenShot
import receiveRunningApp
import receiveProcess
import threading
from GUI import communicate
from GUI import menuScreen
from multiprocessing import Process



def start_client():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = '192.168.2.100'
    host = communicate.ipHost if communicate.ipHost else 'localhost'
    port = 9999
    try:
        clientsocket.connect((host, port))
        communicate.status_connection = 2
        print("Connection succesful")
    except:
        print("Failed to connect")
        clientsocket.close()
        communicate.init()
        return False
    while True:
        # command = input("Enter message to send to server: ")
        while True:
            if communicate.command != '' : 
                command = communicate.command
                break
        clientsocket.send(command.encode('ascii'))
        command = list(map(str, command.split()))
        flag = command[0]
        parameter = -1
        if len(command) > 1 : parameter = command[1]
        
        if flag == "screenshot": receiveScreenShot.readImage(clientsocket)
        elif flag == "saveimage": receiveScreenShot.saveImage()
        elif flag == "listprocess": receiveProcess.receiveProcess(clientsocket)
        elif flag == "killprocess": receiveProcess.receiveStatus(clientsocket)
        elif flag == "listrunningapp": receiveRunningApp.receiveRunningApp(clientsocket)
        elif flag == "shutdown": break
        else:
            data = clientsocket.recv(1024)
            print('Received from server: ', data.decode('ascii'))
        if flag == 'QUIT':
            break
        communicate.command = ''
    clientsocket.close()
    communicate.init()
    return True

def run_client():
    while (communicate.command != "QUIT") and (communicate.status_connection != 1 or not(start_client())): pass

if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_client)
    backend_thread.start()
    menuScreen.run_GUI()
    
    # start_client()