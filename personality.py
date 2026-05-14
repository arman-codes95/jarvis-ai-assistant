import random
from datetime import datetime

def greeting():
    hour = datetime.now().hour
    
    if hour < 12:
        return "Good morning. All systems are fully operational."
    elif hour < 18:
        return "Good afternoon. Systems are running smoothly."
    else:
        return "Good evening. I am at your service."

def acknowledge():
    return random.choice([
        "Certainly.",
        "Right away.",
        "As you wish.",
        "At once.",
        "Immediately."
    ])

def thinking():
    return random.choice([
        "Analyzing request.",
        "Processing.",
        "Let me check that.",
        "One moment."
    ])

def greeting(username, title):
    hour = datetime.now().hour

    if hour < 12:
        part = "Good morning"
    elif hour < 18:
        part = "Good afternoon"
    else:
        part = "Good evening"

    return f"{part}, {username.capitalize()} {title}. Systems are fully operational."

def unknown():
    return random.choice([
        "I’m afraid I did not quite understand that.",
        "Could you please clarify your request?",
        "That command is currently outside my capabilities."
    ])