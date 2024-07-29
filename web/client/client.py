import socket
import threading
import time

class Client:
    HOST = "localhost"
    PORT = 1234
    ADDR = (HOST, PORT)
    BUFSIZE = 512

    def __init__(self, name):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect(self.ADDR)
        self.alive = True
        self.messages = []
        self.lock = threading.Lock()

        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        self.send_message(name)

    def receive_messages(self):
        while self.alive:
            try:
                new_message = self.client_sock.recv(self.BUFSIZE).decode("utf-8")
                if new_message:
                    with self.lock:
                        self.messages.append(new_message)
                    # print(new_message)
                else:
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        self.alive = False

    def send_message(self, msg):
        try:
            self.client_sock.send(bytes(msg, "utf-8"))
            if msg == "{quit}":
                time.sleep(0.1)
                print("Closing connection ....")
                self.client_sock.close()
                self.alive = False
        except Exception as e:
            print(f"Error sending message: {e}")
            self.alive = False

    def get_messages(self):
        with self.lock:
            messages_copy = self.messages[:]
            self.messages = []
        return messages_copy

    def disconnect(self):
        if self.alive:
            self.send_message("{quit}")

