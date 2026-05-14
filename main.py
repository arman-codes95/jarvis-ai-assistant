from voice import speak, listen, stop_speaking
from brain import process
from personality import greeting
import requests

def get_logged_user():
    try:
        r = requests.get("http://127.0.0.1:5000/user")
        data = r.json()
        return data["username"], data["title"]
    except:
        return "User", "Sir"


username, title = get_logged_user()

speak(greeting(username, title))

while True:
    try:
       command = listen()
    except Exception as e:
       print("Microphone error:", str(e))
       continue

    if command:
        if "stop" in command:
            stop_speaking()
            continue

        response = process(command)
        speak(response)