import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import sys
import requests
import random
import time
import re

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# === TEXT TO SPEECH SETUP ===
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Male voice

def talk(text):
    print("🎙️ Ashok:", text)
    engine.say(text)
    engine.runAndWait()

# === LISTENING FUNCTION ===
def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
    try:
        command = listener.recognize_google(voice)
        command = command.lower()
        print("🗣️ You said:", command)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        talk("Network issue with Google service.")
        return ""
    return command

# === FUN FACT FEATURE ===
facts = [
    "Honey never spoils.",
    "Bananas are berries, but strawberries aren’t.",
    "Octopuses have three hearts.",
    "A bolt of lightning can toast 100,000 slices of bread."
]
def tell_fun_fact():
    talk("Here's a fun fact:")
    talk(random.choice(facts))

# === MOTIVATIONAL QUOTES ===
quotes = [
    "Believe in yourself and all that you are.",
    "Push yourself, because no one else is going to do it for you.",
    "Dream big and dare to fail.",
    "Success is not for the lazy.",
    "Great things never come from comfort zones."
]

# === VOLUME FEATURE ===
def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
    except Exception as e:
        talk("Volume control failed.")
        print("Volume Error:", e)

# === CALCULATOR FEATURE ===
def calculate(expression):
    expression = expression.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
    try:
        result = eval(expression)
        talk(f"The answer is {result}")
    except:
        talk("Sorry, I couldn't calculate that.")

# === WHATSAPP MESSAGE FEATURE ===
def send_whatsapp_message():
    talk("Who should I send the message to? Please say the phone number with country code.")
    phone = take_command().replace(" ", "").replace("+", "")
    if not phone.startswith("91"):
        phone = "91" + phone
    phone = "+" + phone

    talk("What is the message?")
    message = take_command()

    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute + 1  # Send 1 minute later

    try:
        pywhatkit.sendwhatmsg(phone, message, hour, minute, wait_time=10, tab_close=True)
        talk("Message scheduled on WhatsApp.")
    except Exception as e:
        print(e)
        talk("Sorry, I couldn't send the message.")

# === FILE READER FEATURE ===
def read_file():
    talk("Say the file name with extension.")
    filename = take_command().strip()
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
            talk("Reading the file:")
            talk(content)
    else:
        talk("Sorry, that file does not exist.")

# === MAIN ASSISTANT LOGIC ===
def run_teju(command):
    if "play" in command:
        song = command.replace("play", "").strip()
        talk(f"Playing {song} on YouTube 🎶")
        pywhatkit.playonyt(song)

    elif "what's the time" in command or "time" in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"It’s {time_now} ⏰")

    elif "who is ravi teja" in command or "who is raviteja" in command:
        talk("Ravi Teja is the creator of this personal voice assistant, Ashok.")
        talk("He is currently pursuing B.Tech in Artificial Intelligence and machine learning at Kalasalingam University.")
        talk("He is passionate about coding, automation, and building AI-powered tools.")


    elif "who is" in command:
        person = command.replace("who is", "").strip()
        try:
            info = wikipedia.summary(person, sentences=1)
            talk(info)
        except:
            talk("Sorry, I couldn’t find information about that person.")

    elif "joke" in command:
        talk(pyjokes.get_joke())

    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            talk("Opening Chrome 🚀")
            os.startfile(chrome_path)
        else:
            talk("Chrome path not found 😬")

    elif "open code" in command or "open vs code" in command:
        talk("Opening VS Code 💻")
        os.system("code")

    elif "fun fact" in command:
        tell_fun_fact()

    elif "motivate" in command or "motivation" in command:
        talk("Here's a motivation for you:")
        talk(random.choice(quotes))

    elif "set a timer" in command:
        talk("For how many seconds?")
        seconds_input = take_command()
        try:
            seconds = int(seconds_input)
            talk(f"Setting a timer for {seconds} seconds ⏳")
            time.sleep(seconds)
            talk("Time's up! 🔔")
        except ValueError:
            talk("That wasn’t a valid number.")

    elif "volume" in command:
        talk("What volume level? Say a number from 0 to 100.")
        level_cmd = take_command()
        try:
            level = int(level_cmd)
            set_volume(level)
            talk(f"Volume set to {level}%.")
        except:
            talk("I didn’t understand the volume level.")

    elif "take a note" in command or "remember this" in command:
        talk("What should I write down?")
        note = take_command()
        with open("notes.txt", "a") as file:
            file.write(f"{note}\n")
        talk("Noted it down 📝")

    elif "read notes" in command or "show notes" in command:
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r") as file:
                notes = file.readlines()
                if notes:
                    talk("Here are your notes:")
                    for line in notes:
                        talk(line.strip())
                else:
                    talk("Your notes file is empty.")
        else:
            talk("You haven’t saved any notes yet.")

    elif "calculate" in command:
        expression = command.replace("calculate", "").strip()
        calculate(expression)

    elif "send message" in command or "whatsapp" in command:
        send_whatsapp_message()

    elif "read file" in command:
        read_file()

    elif "exit" in command or "stop" in command:
        talk("Okay bro, see you later 👋")
        sys.exit()

    elif command != "":
        talk("I heard you, but I don’t understand that yet 😅")

# === STARTUP WITH WAKE WORD ===
talk("Yo! I'm Ashok – your personal voice assistant 💡")
while True:
    command = take_command()
    if "ashok" in command:
        command = command.replace("ashok", "").strip()
        run_teju(command)
