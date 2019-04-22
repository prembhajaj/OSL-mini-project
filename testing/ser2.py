from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_conn():
    
    while True:
        client, client_address = SERVER.accept()
        print("%s has connected." % client_address[0])
 
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_address,)).start()


def handle_client(client,client_address):  
    

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! To quit, type {quit}' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            print("%s left"%client_address[0])
            break


def broadcast(msg, name=""):  
    

    for sock in clients:
        sock.send(bytes(name, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = ''
PORT = 33001
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_conn)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()
