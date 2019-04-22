from socket import *
from threading import Thread
import tkinter
import time

def sf2():
   client_socket.send(bytes(my_msg.get(),"utf8")) 


def sendfile(event=None):

    if my_msg.get() == "{quit}":
        client_socket.close()
        top.destroy()
    msg1="Sent a file. Please Check your folder"
    client_socket.send(bytes(msg1,"utf8"))
    
    f=open(my_msg.get(),"r")
    
    msg1=f.read()
    print(msg1)
    f.close()
    fp=my_msg.get()+"?"
    msg1=fp+msg1
    my_msg.set("")
    client_socket.send(bytes(msg1,"utf8"))

    
    

i=1        
def receivefile():
    global i
    
    
    
    
    
    print(i)



def receive():
    
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")                
            msg_list.insert(tkinter.END, msg)
            if "Sent a file. Please Check your folder" in msg:
                global i
                msg2 = client_socket.recv(BUFSIZ).decode("utf8")
                print(msg2)
##                msgname = client_socket.recv(BUFSIZ).decode("utf8")
##                print(msgname)
                a=msg2.find(":")
                x=msg2[0:a+2]
                msg2=msg2.replace(x,"")
                b=msg2.find("?")
                msgname=msg2[0:b]
                y=msg2[0:b+1]
                msg2=msg2.replace(y,"")
                print(msgname)
                print(msg2)
                f=open(msgname,"w+")

                f.write(msg2)
                f.close()
                
                
##                i+=1
            
                    
            
            
        except OSError:  
            break


def send(event=None):  
    
    msg = my_msg.get()
    my_msg.set("")  
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.destroy()


def on_closing(event=None):
    
    
    my_msg.set("{quit}")
    send()
    #client_socket.close()
    

top1=tkinter.Tk()
top1.title("Chat&Share")
getip = tkinter.StringVar()
getport = tkinter.StringVar()
tkinter.Label(top1,text="Enter host",font="Courier 12 bold",fg="black").grid(row=0,column=0)

tkinter.Entry(top1,textvariable=getip,justify= tkinter.CENTER,width=30,bg="PeachPuff",fg="black").grid(row=0,column=1)
tkinter.Label(top1,text="Enter port",font="Courier 12 bold",fg="black").grid(row=1,column=0)
tkinter.Entry(top1,textvariable=getport,justify= tkinter.CENTER,width=30,bg="PeachPuff",fg="black").grid(row=1,column=1)
tkinter.Button(top1,text="Connect",command=top1.destroy).grid(column=1)
top1.mainloop()


top = tkinter.Tk()
top.title("Chat&Share")

messages_frame = tkinter.Frame(top,borderwidth=10)
my_msg = tkinter.StringVar()  
my_msg.set("")
scrollbar1 = tkinter.Scrollbar(messages_frame)  

msg_list = tkinter.Listbox(messages_frame, width=75,height=15, yscrollcommand=scrollbar1.set,font="Calibri 12 bold ",selectbackground="PeachPuff",highlightcolor="black", bg="PeachPuff",fg="black")
scrollbar1.config(command=msg_list.yview)
scrollbar1.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg,justify= tkinter.CENTER,width=30,bg="PeachPuff",fg="black")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
sendfile_button = tkinter.Button(top, text="Send File", command=sendfile)
sendfile_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


HOST = getip.get()
PORT = getport.get()
if not PORT:
    PORT = 33001
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
client_socket.send(bytes(gethostname(), "utf8"))
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() 
