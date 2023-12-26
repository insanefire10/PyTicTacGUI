import socket
import threading
import sys
from tkinter import *
from tkinter import ttk
version = 0.11

#Button Class to make grid easy
class ButtonArray:
    def __init__(self, x, y, p):
        xCoor = x
        yCoor = y
        tabVar = StringVar()
        turn = p
        tabVar.set(table[x][y])
        if table[x][y] != '#':
            gridButton = Button(root, textvariable=tabVar, padx=50, pady=50,font=("Arial", 20), command= lambda: ButtonArray.add(xCoor,yCoor,tabVar,turn),state=DISABLED).grid(row=x+1, column=y+1)
        else:
            gridButton = Button(root, textvariable=tabVar, padx=50, pady=50,font=("Arial", 20), command= lambda: ButtonArray.add(xCoor,yCoor,tabVar,turn)).grid(row=x+1, column=y+1)
        print("Created button " + str(x),str(y))
        
    def add(x,y,bobj, p):
        if p == 1:
            table[x][y] = 'X'
            bobj.set(table[x][y])
            root.destroy()

    
    
            
       

#setup server network config
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, 420))
server.listen(1)


#setting up table
table = [['#','#','#'],['#','#','#'],['#','#','#']]
tableChosen = [[False,False,False],[False,False,False],[False,False,False]]



#reset table functionality for new game
def tableReset():
    global table
    global tableChosen
    table = [['#','#','#'],['#','#','#'],['#','#','#']]
    tableChosen = [[False,False,False],[False,False,False],[False,False,False]]

#print table function to output table to both players
def printTable():
    out = ""
    for x in range(3):
        for y in range(3):
            out = out + str(table[x][y])
        out = out + "\n"
    return out

#control main game functions, which are player turn as well as displaying the current table to host/guest
def game(client):
    p = 1
    while(True):    
        currTable = printTable()
        print(currTable)
        turn(client, p)

        if p == 1:
            p = 0
        else:
            p = 1

def updateTable(p,x,y):
    if p == 1:
        table[x][y] = 'X'
    else:
        table[x][y] = 'O'



#executes the current turn. If host: asks for user input. If Guest: sends message to guest to request input
def turn(client, p):
    if p == 1:
        client.send(f'HostTurn'.encode('ascii'))
        print("Host Turn:")
        global root
        root = Tk()
        root.title("PyTicTac")
        titleGUI = Label(root, text="PyTicTac",pady=30,font=("Segoe UI", 20)).grid(row=0,column=1)
        #button
        grid = [['NULL','NULL','NULL'],['NULL','NULL','NULL'],['NULL','NULL','NULL']]
        for x in range(3):
            for y in range(3):
                grid[x][y] = ButtonArray(x,y,p)
        root.update()
        root.mainloop()

    else:
        
        global table
        #client.send(f'Guest Turn:'.encode('ascii'))
        currTable = printTable()
        client.send(f'{currTable}'.encode('ascii'))
        root = Tk()
        root.title("PyTicTac")
        titleGUI = Label(root, text="PyTicTac\nWaiting for Guest...",pady=30,font=("Segoe UI", 20)).grid(row=0,column=1)
        root.update()
        message = client.recv(1024).decode('ascii')
        root.destroy()
        
        if message == "EXITCODE":
            print("Guest left the game. Closing application")
            exit()
        userX, userY = message.split(" ")
        print(userX)
        print(userY)

        userX = int(userX)
        userY = int(userY)
        
        table[userX][userY] = 'O'
    
    result = checkGame(table)
    if result == "p1":
        root = Tk()
        client.send(f'EXITP1'.encode('ascii'))
        root.title("PyTicTac")
        out = Label(root, text="You Win!",pady=30,font=("Segoe UI", 20)).grid(row=0,column=0)
        out2 = Button(root, text="Exit", padx=50, pady=50,font=("Arial", 20), command=exit).grid(row=1,column=0)
        root.mainloop()
    if result == "p2":
        print("You Lose!")
        client.send(f'EXITP2'.encode('ascii'))
        root = Tk()
        root.title("PyTicTac")
        out = Label(root, text="You Lose",pady=30,font=("Segoe UI", 20)).grid(row=0,column=0)
        out2 = Button(root, text="Exit", padx=50, pady=50,font=("Arial", 20), command=exit).grid(row=1,column=0)
        root.mainloop()
        exit()
    if result == "Tie":
        root = Tk()
        client.send(f'Tie'.encode('ascii'))
        root.title("PyTicTac")
        out = Label(root, text="Tie!",pady=30,font=("Segoe UI", 20)).grid(row=0,column=0)
        out2 = Button(root, text="Exit", padx=50, pady=50,font=("Arial", 20), command=exit).grid(row=1,column=0)
        root.mainloop()
    

#CheckGame will run after every turn to see if the Host/Guest has 3 in a row
def checkGame(table):
    for x in table:
        if (x[0] == x[1]) and (x[1] == x[2]):
            if(x[0] == 'X'):
                return "p1"
            if(x[0] == "O"):
                return "p2"
    for y in range(3):
        if (table[0][y] == table[1][y]) and (table[1][y] == table[2][y]):
            if(table[1][y] == 'X'):
                return "p1"
            if(table[1][y] == "O"):
                return "p2"
    if (table[0][0]==table[1][1]) and (table[1][1] == table[2][2]):
        if(table[1][1] == 'X'):
                return "p1"
        if(table[1][1] == "O"):
            return "p2"
    if (table[0][2]==table[1][1]) and (table[1][1] == table[2][0]):
        if(table[1][1] == 'X'):
            return "p1"
        if(table[1][1] == "O"):
            return "p2"   
        
    flag = 0
    for x in range(3):
        for y in range(3):
            if table[x][y] == '#':
                flag = 1
    if flag == 0:
        return "Tie"

#connection handler
def conn():
    consz.update()
    while(True):
        client, address = server.accept()
        consz.destroy()
        print("Connected to P2")
        client.send(f'Connected to P1'.encode('ascii'))
        game(client)
        


#main
consz = Tk()
print("Welcome to PyTicTac " + str(version))
print("Starting up connection...")
print("Ask guest to enter in these details: ")
print("IP: " + str(host))
print("Port: 420")
consz.title("PyTicTac")
mm1 = Label(consz, text="Welcome to PyTicTac " + str(version),pady=30,font=("Segoe UI", 20)).grid(row=0,column=0)
mm2 = Label(consz, text="Starting up connection...",pady=30,font=("Segoe UI", 20)).grid(row=1,column=0)
mm3 = Label(consz, text="Ask guest to enter in these details: ",pady=30,font=("Segoe UI", 20)).grid(row=2,column=0)
mm4 = Label(consz, text="IP: " + str(host),pady=30,font=("Segoe UI", 20)).grid(row=3,column=0)
mm5 = Label(consz, text="Port: 420",pady=30,font=("Segoe UI", 20)).grid(row=4,column=0)

conn()
