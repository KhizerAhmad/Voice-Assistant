# Jarvis — Python Voice Assistant 🎙️

A voice-controlled assistant built in Python that actually does stuff — web searches, news updates, playing music, opening websites, and answering questions using Google Gemini AI. Just talk to it and it responds.

---

## What it does

- Listens for voice commands using speech recognition
- Performs web searches via Selenium browser automation
- Fetches latest news from a News API
- Opens websites on command
- Plays music from a custom music library
- Answers general questions using Google Gemini AI
- Responds back with text-to-speech (TTS)

---

## Why I built this

Wanted to go beyond basic Python scripts and build something that ties together multiple real tools — speech recognition, browser automation, an AI API, and a news API — all in one working project. Jarvis was the obvious theme.

---

## Tech Stack

| Library / Tool | Usage |
|----------------|-------|
| Python | Core language |
| SpeechRecognition | Listening to voice input |
| pyttsx3 / TTS | Speaking responses out loud |
| Selenium | Browser automation for web searches |
| Google Gemini AI | Answering open-ended questions |
| News API | Fetching latest headlines |
| webbrowser | Opening websites |
| musicLib.py | Custom music library module |

---

## Project Structure

```
Jarvis Assistant/
│
├── main.py          # Core assistant logic and command handling
├── musicLib.py      # Music library — song names mapped to URLs/paths
├── requirements.txt # All dependencies
└── .gitignore
```

---

## Setup & Installation

**1. Clone the repo**
```bash
git clone https://github.com/KhizerAhmad/Voice-Assistant.git
cd Jarvis Assistant
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API keys**

You'll need:
- A **Google Gemini API key** — get it from [Google AI Studio](https://aistudio.google.com)
- A **News API key** — get it from [newsapi.org](https://newsapi.org)

Add them to `main.py` where the API keys are configured.

**4. Run it**
```bash
python main.py
```

---

## How to use it

Once running, just speak a command. Examples:

| Voice Command | What happens |
|---------------|--------------|
| "Search Python tutorials" | Opens browser and searches |
| "What's the news today" | Reads out latest headlines |
| "Play [song name]" | Plays the song from musicLib |
| "Open YouTube" | Opens YouTube in browser |
| "What is machine learning" | Gemini AI answers the question |

---

## Requirements

- Python 3.8+
- A working microphone
- Chrome browser (for Selenium)
- ChromeDriver matching your Chrome version

---


## Author

**Khizer Ahmad** — built this to get hands-on with speech recognition, browser automation, and AI API integration in a single practical Python project.

Feel free to fork it and add your own commands.
