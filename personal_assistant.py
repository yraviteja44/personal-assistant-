import sys
import random
import time
import pyautogui
import cv2
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
from deep_translator import GoogleTranslator

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# === TEXT TO SPEECH SETUP ===
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  

def talk(text):
    print("\U0001F399\uFE0F Ashok:", text)
    engine.say(text)
    engine.runAndWait()

# === LISTENING FUNCTION ===
def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("\U0001F3A7 Listening...")
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
    try:
        command = listener.recognize_google(voice)
        command = command.lower()
        print("\U0001F5E3\uFE0F You said:", command)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        talk("Network issue with Google service.")
        return ""
    return command

def translate_text():
    talk("What text do you want to translate?")
    text = take_command()
    if text == "":
        talk("Sorry, I couldn't hear the text.")
        return

    talk("Which language should I translate to? For example, say Hindi, French, or Telugu.")
    target = take_command()

    lang_map = {
        "english": "en",
        "hindi": "hi",
        "french": "fr",
        "spanish": "es",
        "german": "de",
        "tamil": "ta",
        "telugu": "te",
        "kannada": "kn",
        "malayalam": "ml"
    }

    lang_code = next((lang_map[lang] for lang in lang_map if lang in target.lower()), None)

    if not lang_code:
        talk("Sorry, I don't support that language yet.")
        return

    try:
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
        talk(f"The translation in {target.title()} is:")
        talk(translated)
    except:
        talk("Translation failed. Please try again later.")

# === MAIN ASSISTANT LOGIC ===
def handle_command(command):
    if "play" in command:
        song = command.replace("play", "").strip()
        talk(f"Playing {song} on YouTube \U0001F3B6")
        pywhatkit.playonyt(song)

    elif "what's the time" in command or "time" in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"It is {time_now} ⏰")

    elif "who is ravi teja" in command or "who is teju" in command:
        talk("He is a kind individual from Dharmavaram currently pursuing a B.Tech degree.")

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
            talk("Opening Chrome \U0001F680")
            os.startfile(chrome_path)
        else:
            talk("Chrome path not found.")

    elif "open code" in command or "open vs code" in command:
        talk("Opening Visual Studio Code \U0001F4BB")
        os.system("code")

    elif "fun fact" in command:
        talk("Here's a fun fact:")
        facts = [
            "Honey never spoils.",
            "Bananas are berries, but strawberries aren’t.",
            "Octopuses have three hearts.",
            "A bolt of lightning can toast 100,000 slices of bread."
        ]
        talk(random.choice(facts))

    elif "motivate" in command or "motivation" in command:
        quotes = [
            "Believe in yourself and all that you are.",
            "Push yourself, because no one else is going to do it for you.",
            "Dream big and dare to fail.",
            "Success is not for the lazy.",
            "Great things never come from comfort zones."
        ]
        talk("Here's a motivational quote:")
        talk(random.choice(quotes))

    elif "set a timer" in command:
        talk("For how many seconds?")
        seconds_input = take_command()
        try:
            seconds = int(seconds_input)
            talk(f"Setting a timer for {seconds} seconds ⏳")
            time.sleep(seconds)
            talk("Time's up! \U0001F514")
        except ValueError:
            talk("That wasn’t a valid number.")

    elif "volume" in command:
        talk("What volume level? Say a number from 0 to 100.")
        level_cmd = take_command()
        try:
            level = int(level_cmd)
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            talk(f"Volume set to {level} percent.")
        except:
            talk("I didn’t understand the volume level.")

    elif "take a note" in command or "remember this" in command:
        talk("What should I write down?")
        note = take_command()
        with open("notes.txt", "a") as file:
            file.write(f"{note}\n")
        talk("Note saved successfully.")

    elif "read notes" in command or "show notes" in command:
        if os.path.exists("notes.txt"):
            with open("notes.txt", "r") as file:
                notes = file.readlines()
                if notes:
                    talk("Here are your saved notes:")
                    for line in notes:
                        talk(line.strip())
                else:
                    talk("Your notes file is empty.")
        else:
            talk("You haven’t saved any notes yet.")

    elif "calculate" in command:
        expression = command.replace("calculate", "").strip()
        expression = expression.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
        try:
            result = eval(expression)
            talk(f"The answer is {result}")
        except:
            talk("Sorry, I couldn't calculate that.")

    elif "send message" in command or "whatsapp" in command:
        talk("Who should I send the message to? Please say the phone number with country code.")
        phone = take_command().replace(" ", "").replace("+", "")
        if not phone.startswith("91"):
            phone = "91" + phone
        phone = "+" + phone

        talk("What is the message?")
        message = take_command()

        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute + 1
        try:
            pywhatkit.sendwhatmsg(phone, message, hour, minute, wait_time=10, tab_close=True)
            talk("Message scheduled on WhatsApp.")
        except Exception as e:
            print(e)
            talk("Sorry, I couldn't send the message.")

    elif "translate" in command:
        translate_text()

    elif "screenshot" in command:
        talk("Taking screenshot...")
        screenshot = pyautogui.screenshot()
        filename = f"screenshot_{int(time.time())}.png"
        screenshot.save(filename)
        talk(f"Screenshot saved as {filename}.")

    elif "open camera" in command or "click photo" in command:
        talk("Opening camera. Press SPACE to capture or ESC to cancel.")
        cam = cv2.VideoCapture(0)

        while True:
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)
            cv2.imshow("Camera - Press SPACE to capture", frame)

            key = cv2.waitKey(1)
            if key == 27:
                talk("Camera closed.")
                break
            elif key == 32:
                filename = f"photo_{int(time.time())}.jpg"
                cv2.imwrite(filename, frame)
                talk(f"Photo saved as {filename}.")
                break

        cam.release()
        cv2.destroyAllWindows()

    elif "exit" in command or "stop" in command:
        talk("Thank you. Have a nice day!")
        sys.exit()

    elif command != "":
        talk("I heard you, but I do not understand that command yet.")

# === STARTUP WITH WAKE WORD ===
talk("Hello, I am Ashok – your personal voice assistant. How can I assist you today?")
while True:
    command = take_command()
    if "ashok" in command:
        command = command.replace("ashok", "").strip()
        handle_command(command)

