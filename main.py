import random
import time

import requests
import threading

Running = True
Connected = False

url = "https://thomas-chatroom-server.herokuapp.com/"

words_txt = open("ukenglish.txt", "r")
words = words_txt.read().split()
words_length = len(words)
words_txt.close()

names_txt = open("names.txt", "r")
names = names_txt.read().split()
names_length = len(names)
names_txt.close()

def create_client(bot):
    if bot:
        username = names[random.randint(0, names_length)]
    else:
        print("What is your username?")
        username = input()

    def recieving_events():
        global Running, Connected
        while Running:
            try:
                if Connected == False:
                    print("Connected to server")
                    Connected = True
                connection = requests.post(url + "maintain_connection", json={"username": username})
                if connection.status_code != 200:
                    print("Server failed")
                    Running = False

                data = connection.json()["data"]
                if not bot:
                    for d in data:
                        if d["event_type"] == "new_msg":
                            print(f"{d['content']['username']} : {d['content']['message']}")

                        elif d["event_type"] == "new_connection":
                            print(f"{d['content']['username']} has joined the room")

                        elif d["event_type"] == "lost_connection":
                            print(f"{d['content']['username']} has left the room")
                    if not data == []:
                        print("-----------")

            except:
                Connected = False
                print("Failed to contact server")
                time.sleep(5)
                print("Attempting to contact again")

    def sending_events():
        while Running:
            if bot:
                msg = words[random.randint(0, words_length)]
                time.sleep(10)
                sent_message = requests.post(url + "new_msg", json={"username": username, "message": msg})
            else:
                msg = input()
                sent_message = requests.post(url + "new_msg", json={"username": username, "message": msg})

    recieving_events_thread = threading.Thread(target=recieving_events)
    recieving_events_thread.start()

    sending_events_thread = threading.Thread(target=sending_events)
    sending_events_thread.start()

threads = []

for x in range(0, 10):
    threads.append(threading.Thread(target=create_client, args=(True,)))
    threads[x].start()
    print(f"Bot {x} has been created")

create_client(False)

time.sleep(30)