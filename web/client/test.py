from client import Client
import time
import threading

# c1 = Client("p")

# def update_messages():
#     msgs = []
#     run = True
#     while run:
#         try:
#             time.sleep(0.1)
#             new_messages = c1.get_messages()
#             msgs.extend(new_messages)
#             for msg in new_messages:
#                 return msgs
#                 if msg == "{quit}":
#                     run = False
#                     break
#         except Exception as e:
#             print(e)



# if __name__ == "__main__":
#     threading.Thread(target=update_messages, daemon=True).start()

# c1.send_message("Heloo")
# time.sleep(1)
# c2.send_message("jhi!!")
# time.sleep(1)
# c1.send_message("lala")
# time.sleep(1)
# c2.send_message("dododo")
# time.sleep(1)

# c1.disconnect()
# time.sleep(2)
# c2.disconnect()



from client import Client
# # Example usage:
if __name__ == "__main__":
    name =  input("Enter name : ")
    client = Client(name)
    try:
        while client.alive:
            msg = input()
            client.send_message(msg)
            if msg == "{quit}":
                client.disconnect()
                break
    except KeyboardInterrupt:
        client.disconnect()
