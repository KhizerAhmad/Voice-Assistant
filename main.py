import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import musicLib
import requests
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv
from pathlib import Path
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

recognizer = sr.Recognizer()
start = True
env_path = Path("dotenv")
load_dotenv(dotenv_path=env_path)
newsAPI = os.getenv("newsAPI")
geminiAPI = os.getenv("GEMINI_API_KEY")
edge_driver = None


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def speak_old(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init(frequency=44101)
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()


def init_browser():
    global edge_driver
    if edge_driver is None:
        options = Options()
        options.add_argument("--start-maximized")
        service = Service("msedgedriver.exe")
        edge_driver = webdriver.Edge(options=options, service=service)


def aiProcess(c):
    genai.configure(api_key=geminiAPI)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(c)
    return response.text


def selenium_google_search(query):
    init_browser()
    driver = edge_driver
    driver.get("https://www.google.com")
    time.sleep(1)
    searchBar = driver.find_element(By.NAME, "q")
    searchBar.clear()
    searchBar.send_keys(query)
    searchBar.send_keys(Keys.RETURN)
    time.sleep(2)
    first_result = driver.find_element(By.CSS_SELECTOR, "h3")
    first_result.click()
    return first_result


def processCommand(c):
    if c.lower().startswith("search for"):
        query = c.replace("search for", "").strip()
        selenium_google_search(query)
        speak(f"Here is what i found for {query}")
    elif "open google" in c.lower():
        init_browser()
        edge_driver.get("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open github" in c.lower():
        webbrowser.open("https://www.github.com")
    elif c.lower().startswith("open"):
        secondWord = c.lower().split(" ")[1]
        webbrowser.open(f"https://www.{secondWord}.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        if song in musicLib.musics:
            link = musicLib.musics[song]
            webbrowser.open(link)
        else:
            speak("Sorry boss song not found: ")
            print(f"Available Songs: {musicLib.musics.keys()}")
    elif "news" in c.lower():
        try:
            api = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsAPI}")
            if (api.status_code == 200):
                data = api.json()
                articles = data["articles"]
                titles = list(
                    map(lambda article: article["title"], articles[:5]))
                speak(f"Here are the top {len(titles)} headlines: ")
                for i, title in enumerate(titles, 1):
                    title = title.split("-")[0]
                    speak(f"Headline {i}. {title}")
                    print(i, title, sep=" -> ")
            else:
                speak("Sorry, Cant Fetch headlines right now. ")
                print(f"Status code: {api.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    time.sleep(1)
    while start:
        r = sr.Recognizer()
        print("Listening...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Recognizing...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            print(f"You said: {word}")
            if ("jarvis" in word.lower()):
                speak("Yes boss")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
            if ("bye" in word.lower()):
                speak("Ok boss see you tomorrow: ")
                start = False
        except sr.UnknownValueError as e:
            print("Could not understand Audio: ")
        except sr.WaitTimeoutError as e:
            print("No Audio was detected in that time-period: ")
        except KeyboardInterrupt:
            print("Existing Jarvis...")
            break
        except Exception as e:
            print(f"Error: {e}")
