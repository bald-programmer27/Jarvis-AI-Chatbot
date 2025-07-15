import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import threading
import requests
import time
import random
from googletrans import Translator

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Dictionary to store client names and their email
clients = {
    "ali": "alirabeet52@gmail.com",
    "hamza": "hamzabjaved04@gmail.com",
    "zarak": "zarakomer12@gmail.com",
}

# Functions
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('subha bakhair')
    elif hour >= 12 and hour < 18:
        speak('kia khoobsurat din hai')
    else:
        speak('shaam ho chuki hai')
    speak('How can I help you, sir?')

def takeCommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
    except sr.RequestError:
        speak("Microphone not detected or unavailable.")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        speak("Something went wrong. Please try again.")
        return "None"
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        return "None"
    return query

def take_picture():
    cap = cv2.VideoCapture(0)
    speak("Taking your picture.")
    ret, frame = cap.read()
    if ret:
        filename = os.path.join(os.path.expanduser("~"), "Pictures", "captured_image.jpg")
        cv2.imwrite(filename, frame)
        speak(f"Picture saved as {filename}.")
    else:
        speak("Sorry, I couldn't take the picture.")
    cap.release()
    cv2.destroyAllWindows()

def record_video():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = os.path.join(os.path.expanduser("~"), "Videos", "recorded_video.avi")
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
    speak("Recording video. Say stop recording to end.")
    while True:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    speak(f"Video saved as {filename}.")

#For Google
def search(g_search):
    query=g_search.replace(" ", "+")
    url=f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def get_weather(city_name):
    api_key = "ed1cd69b15824d16e5f72d12fbad1d34"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temp = main["temp"]
        humidity = main["humidity"]

        weather_report = (
            f"The weather in {city_name} is currently {weather_desc} "
            f"with a temperature of {temp}°C and a humidity of {humidity}%."
        )
        return weather_report
    else:
        return f"Sorry, I couldn't find the weather information for {city_name}."

def speak_weather(city_name):
    weather = get_weather(city_name)
    speak(weather)

#For Calculator
def get_number(prompt):
    speak(prompt)
    while True:
        number = takeCommand()
        try:
            return float(number)
        except ValueError:
            speak("That doesn't seem to be a valid number, Please say it again")


def get_operator():
    speak("Please say the operator you want to use.")
    while True:
        operator = takeCommand().lower()
        if operator in ["plus", "addition", "add", "+"]:
            return "+"
        elif operator in ["minus", "subtraction", "subtract", "-"]:
            return "-"
        elif operator in ["multiply", "multiplication", "times", "*"]:
            return "*"
        elif operator in ["divide", "division", "divided by","divides", "/"]:
            return "/"
        else:
            speak("Invalid operator. Please say it again.")


def calculator():
    speak("Welcome to the voice calculator")
    first_number = get_number("Please say the first number.")
    second_number = get_number("Please say the second number.")
    operator = get_operator()

    if operator == "+":
        result = first_number + second_number
    elif operator == "-":
        result = first_number - second_number
    elif operator == "*":
        result = first_number * second_number
    elif operator == "/":
        if second_number == 0:
            speak("Division by zero is not allowed.")
            print("Division by zero is not allowed.")
            return
        result = first_number / second_number

    speak(f"The result of {first_number} {operator} {second_number} is {result}")
    print(f"The result of {first_number} {operator} {second_number} is {result}")

    #For Stopwatch
def start_stopwatch():
    speak("Stopwatch started. Say 'stop' to stop the stopwatch.")
    start_time = time.time()
    
    while True:
        command = takeCommand()  
        if 'stop' in command.lower():
            elapsed_time = time.time() - start_time
            mins, secs = divmod(elapsed_time, 60)
            speak(f"Stopwatch stopped. Total time: {int(mins)} minutes and {int(secs)} seconds.")
            break
from googletrans import Translator  # Ensure this import is present

def translate_text(text, dest_language):  # 'text' is text to be translated and 'dest_language' is the target language code
    translator = Translator()  # Create Translator object
    try:
        translated = translator.translate(text, dest=dest_language)  # Translate the input text
        return translated.text  # Return the translated text
    except Exception as e:
        speak("Sorry, I couldn't translate the text.")
        print("Translation error:", e)
        return None

def animate_mic():
    global grow
    if grow:
        size[0] += 5
        size[1] += 5
        if size[0] >= 150:
            grow = False
    else:
        size[0] -= 5
        size[1] -= 5
        if size[0] <= 100:
            grow = True

    resized_image = mic_image.resize((size[0], size[1]))
    mic_photo = ImageTk.PhotoImage(resized_image)
    mic_label.config(image=mic_photo)
    mic_label.image = mic_photo

    root.after(100, animate_mic)

def open_youtube_link(query):
    query = query.replace("youtube", "").strip()
    speak("Searching YouTube...")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def run_jarvis():
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'exit' in query.lower():
            speak('Goodbye!')
            root.quit()
            break

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open proposal' in query:
            codePath = "C:\\Users\\CS\\OneDrive\\Desktop\\AI project"
            os.startfile(codePath)
        elif 'open instagram' in query:
            webbrowser.open('instagram.com')
        elif 'open github' in query:
            webbrowser.open('github.com')
        elif 'open facebook' in query:
            webbrowser.open('facebook.com')
        elif 'open neetcode' in query:
            webbrowser.open('neetcode.com')
        elif 'open yahoo' in query:
            webbrowser.open('yahoo.com')
        elif 'open chat gpt' in query:
            webbrowser.open('chatgpt.com')
        elif 'take my picture' in query:
            take_picture()
        elif 'record video' in query:
            record_video()
        elif 'open word' in query:
            wordpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            os.startfile(wordpath)  
        elif 'open excel' in query:
            excelpath="C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
            os.startfile(excelpath)
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'youtube' in query:
            open_youtube_link(query)
        elif 'tell weather' in query:
            speak("Which city's weather would you like to know?")
            city_name = takeCommand()
            speak_weather(city_name)

        elif 'search on google' in query:
            speak("What do you want to search?")
            search_bar=takeCommand()
            search(search_bar)    

        elif 'calculator' in query:
            calculator()   

        elif 'start stopwatch' in query:
            start_stopwatch()  

        elif 'translate' in query:
            speak("What text would you like me to translate?")
            text_to_translate = takeCommand()
            if text_to_translate == "None":
                continue
            speak("Which language should I translate it to?")
            language = takeCommand().lower()
            language_mapping = {
                "french": "fr",
                "spanish": "es",
                "german": "de",
                "italian": "it",
                "hindi": "hi",
                "arabic": "ar",
                "chinese": "zh-cn",
                "japanese": "ja",
                "russian": "ru",
            }
            dest_language = language_mapping.get(language, None)  #Takes the user-provided language name and retrieves the corresponding language code from the language_mapping dictionary
            if not dest_language:
                speak("Sorry, I don't recognize that language.")
                continue
            translated_text = translate_text(text_to_translate, dest_language)
            if translated_text:
                speak(f"The translation is: {translated_text}")
                print(f"Translated text: {translated_text}")    
            

if __name__ == "__main__":
    if not os.path.exists("me.jpg"):
        print("Error: 'me.jpg' not found. Please place the image in the same directory as the script.")
        exit()

    root = tk.Tk()
    root.title("Jarvis")
    root.geometry("400x400")
    root.configure(bg="orange")

    mic_image = Image.open("me.jpg")
    size = [100, 100]
    mic_photo = ImageTk.PhotoImage(mic_image.resize(size))
    mic_label = tk.Label(root, image=mic_photo, bg="orange")
    mic_label.pack(expand=True)

    grow = True
    animate_mic()

    jarvis_thread = threading.Thread(target=run_jarvis, daemon=True)
    jarvis_thread.start()

    root.mainloop()
