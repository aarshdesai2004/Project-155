
from tkinter import *
from threading import Thread
import socket

#nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height = 300)
        
        self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
        self.pls.place( relheight = 0.15,
                        relx = 0.2,
                        rely = 0.07)

        self.labelName = Label(self.login,
							text = "Name: ",
							font = "Helvetica 12")
        self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.2)
        self.entryName = Entry(self.login,
							font = "Helvetica 14")
        self.entryName.place(relwidth= 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
        self.entryName.focus()
        self.go = Button(self.login,text='Continue',font=('Helvetica' ,12),command= lambda : self.goahead(self.entryName.get()))
        self.go.place(relx=0.4,rely=0.55)
        self.Window.mainloop()  
    def goahead(self,name):
        self.login.destroy()
        self.layout(name)
        receive_thread = Thread(target=self.receive)
        receive_thread.start()
    def layout(self,name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
							height = False)
        self.Window.configure(width = 470,
							height = 550,
							bg = "#17202A")
        self.labelHead = Label(self.Window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = self.name ,
							font = "Helvetica 13 bold",
							pady = 5)
		
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
						width = 450,
						bg = "#ABB2B9")
		
        self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
        self.textCons = Text(self.Window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
		
        self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
        self.labelBottom = Label(self.Window,bg='#ABB2B9',height = 80)
        self.labelBottom.place(relwidth=1,rely=0.825)

        self.entryMessage = Entry(bg = "#2C3E50", fg = "#EAECEE", font = "Helvetica 13")
        self.entryMessage.place(relwidth = 0.74, relheight = 0.06, rely = 0.008, relx = 0.011)
        self.entryMessage.focus()
        self.textCons.configure(cursor='arrow')
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight = 1, relx = 0.974) 
        scrollbar.config(command = self.textCons.yview)
        self.button =  Button(self.labelBottom,text='Send',font = "Helvetica 10 bold", width = 20, bg = "#ABB2B9",command=lambda : self.sendButton(self.entryMessage.get()))
        self.button.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22)   
    def sendButton(self,message):
        self.textCons.config(state=DISABLED)
        self.message = message
        self.entryMessage.delete(0,END)
        write_thread = Thread(target=self.write)
        write_thread.start()
        self.textCons.config(state=DISABLED)
        self.message = message
        self.entryMessage.delete(0,END)
        write_thread = Thread(target=self.write)
        write_thread.start()
        
    def showmessage(self,message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,message+'\n\n')
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f'{self.name} : {self.message}')	
            client.send(message.encode('utf-8'))
            self.showmessage(message)
            break

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                  client.send(self.name.encode('utf-8'))
                else:
                  self.showmessage(message)
            except:
                   print("An error occured!")
                   client.close()
                   break     
g = GUI()
                      
    


