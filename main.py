import time

import requests
import threading

Running = True
Connected = False

url = "https://thomas-chatroom-server.herokuapp.com/"

print("What is your username?")
username = input(">>> ")

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

            for d in data:
                if d["event_type"] == "new_msg":
                    print(f"{d['content']['username']} : {d['content']['message']}")

                elif d["event_type"] == "new_connection":
                    print(f"{d['content']['username']} has joined the room")

                elif d["event_type"] == "lost_connection":
                    print(f"{d['content']['username']} has left the room")
        except:
            Connected = False
            print("Failed to contact server")
            time.sleep(5)
            print("Attempting to contact again")

def sending_events():
    while Running:
        msg = input()
        sent_message = requests.post(url + "new_msg", json={"username": username, "message": msg})

recieving_events_thread = threading.Thread(target=recieving_events)
recieving_events_thread.start()

sending_events_thread = threading.Thread(target=sending_events)
sending_events_thread.start()
