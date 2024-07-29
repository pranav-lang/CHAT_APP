import socket
import threading
from person import Person

# GLOBAL CONSTANTS
HOST = "localhost"
PORT = 1234
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZE = 512

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

# GLOBAL VARIABLES
persons = []




def broadcast(msg, name="server"):
    for person in persons:
        try:
            person.client.send(bytes(name + ": ", "utf-8") + msg)
        except Exception as e:
            print(f"Error sending message to {person.name}: {e}")

def client_communication(person):
    client = person.client
    addr = person.addr

    try:
        name = client.recv(BUFSIZE).decode("utf-8")  # First message from the poerson would be the name
        person.set_name(name)

        msg = f"{name} has joined the chat!".encode("utf-8")  # Welcome Message
        print(msg.decode("utf-8"))
        broadcast(msg)  # sends message to everyone ( cleint ) in the persons  list

        while True:  # loop to recieve every other messages
            msg = client.recv(BUFSIZE)

            if msg == bytes("{quit}", "utf-8"): # disconnect with the client if the message is {quit}
                client.close()
                persons.remove(person)
                broadcast(f"{name} has left the chat...".encode("utf-8"))
                print(f"[DISCONNECTED] {name} disconnected..")
                break
            else:
                print(f"{name} : {msg.decode("utf-8")}")  # else broadcast it to everybody
                broadcast(msg, name)
    except Exception as e:
        print(f"Error handling communication with {addr}: {e}")
    finally:
        if person in persons:
            persons.remove(person)
        client.close()

def wait_for_connection():
    while True:
        try:
            client, addr = SERVER.accept() # wait for a new connection..
            person = Person(addr, client)
            persons.append(person)
            threading.Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[FAILURE]:", e)
            break
    print("SERVER crashed..")

if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)
    print("[STARTED] Waiting for connection.")
    ACCEPT_THREAD = threading.Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()
