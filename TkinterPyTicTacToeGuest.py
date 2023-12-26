import socket
import threading
import sys
from tkinter import *
import time

version = 0.11
table = [['#','#','#'],['#','#','#'],['#','#','#']]

#Button Class to make grid easy
class ButtonArray:
    def __init__(self, x, y):
        xCoor = x
        yCoor = y
        tabVar = StringVar()
        tabVar.set(table[x][y])
        if table[x][y] != '#':
            gridButton = Button(root, textvariable=tabVar, padx=50, pady=50,font=("Arial", 20), command= lambda: ButtonArray.add(xCoor,yCoor,tabVar),state=DISABLED).grid(row=x+1, column=y+1)
        else:
            gridButton = Button(root, textvariable=tabVar, padx=50, pady=50,font=("Arial", 20), command= lambda: ButtonArray.add(xCoor,yCoor,tabVar)).grid(row=x+1, column=y+1)
    def add(x,y,bobj):
        if True:
            table[x][y] = 'O'
            bobj.set(table[x][y])
            root.destroy()
            out = str(x) + " " + str(y)
            sendCoordinate(out)


root = Tk()
root.title("PyTicTac")
title = Label(root, text="Welcome to PyTicTac!",pady=30,font=("Segoe UI", 20)).grid(row=0,column=0)
title = Label(root, text="Enter The host IP: ",pady=30,font=("Segoe UI", 20)).grid(row=1,column=0)
title = Label(root, text="Enter Port number: ",pady=30,font=("Segoe UI", 20)).grid(row=2,column=0)

hostIn = StringVar()
portIn = StringVar()
e1 = Entry(root,textvariable=hostIn).grid(row=1,column=1)

e2 = Entry(root,textvariable=portIn).grid(row=2,column=1)

continueButton = Button(root, text="Enter Game", command=root.destroy).grid(row=3)

root.mainloop()

host = hostIn.get()
port = portIn.get()
port = int(port)
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
except:
    print("Connection failed, please ENTER to exit")
    dummy = input("")
    exit()

def tableCreate(msg):
    global table
    table = [[msg[0],msg[1],msg[2]],[msg[4],msg[5],msg[6]],[msg[8],msg[9],msg[10]]]

def receive():

    while(True):
        try:
            root2 = Tk()
            root2.title("PyTicTac")
            titleGUI = Label(root2, text="PyTicTac\nWaiting for Host...",pady=30,font=("Segoe UI", 20)).grid(row=0,column=1)
            root2.update()
            message = client.recv(1024).decode('ascii')
            root2.destroy()
            print(message)
            print(type(message))
            if message == "Guest Turn":
                print("Guest Turn")
                continue
            elif message == "EXITP1":
                print("You Lose!")
                rootOut1 = Tk()
                rootOut1.title("PyTicTac")
                out = Label(rootOut1, text="You Lose!",pady=30,font=("Segoe UI", 20)).grid(row=0,column=0)
                out2 = Button(rootOut1, text="Exit", padx=50, pady=50,font=("Arial", 20), command=exit).grid(row=1,column=0)
                rootOut1.mainloop()
                exit()
            elif message == "EXITP2":
                print("You Win!")
                rootOut2 = Tk()
                rootOut2.title("PyTicTac")
                out = Label(rootOut2, text="You Win!",pady=30,font=("Segoe UI", 20)).grid(row=0,column=0)
                out2 = Button(rootOut2, text="Exit", padx=50, pady=50,font=("Arial", 20), command=exit).grid(row=1,column=0)
                rootOut2.mainloop()
                exit()
            elif message == "Tie":
                rootOut3 = Tk()
                rootOut3.title("PyTicTac")
                out = Label(rootOut3, text="Tie!",pady=30,font=("Segoe UI", 20)).grid(row=0,column=0)
                out2 = Button(rootOut3, text="Exit", padx=50, pady=50,font=("Arial", 20), command=exit).grid(row=1,column=0)
                rootOut3.mainloop()
            if '#' in message:
                print(message)
                tableCreate(message)
                global table
                global root
                root = Tk()
                root.title("PyTicTac")
                print(table)
                titleGUI = Label(root, text="PyTicTac",pady=30,font=("Segoe UI", 20)).grid(row=0,column=1)
                #button
                grid = [['NULL','NULL','NULL'],['NULL','NULL','NULL'],['NULL','NULL','NULL']]
                for x in range(3):
                    for y in range(3):
                        grid[x][y] = ButtonArray(x,y)
                root.update()
                root.mainloop()


        except:
            print("ERROR")
            client.close()
            exit()

def sendCoordinate(GuestTurn):
    client.send(f'{GuestTurn}'.encode('ascii'))

receive()


