
# API KEY AIzaSyBLESC0RMLk5RKPg3aSeqCVZd1NEWAMj7A

# Author: Giancarlos Minyetti
# Description: Jarvis AI Helment 
# Date: 10/1/25

# Install the SDK (if not already installed):
# pip install -U google-generativeai
# pip install google-generativeai pyttsx3

# CONFIGRATION File

import google.generativeai as genai
import pyttsx3
import os
import time
import re

#  CONFIGRATION AI

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBLESC0RMLk5RKPg3aSeqCVZd1NEWAMj7A")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-2.5-flash")

engine = pyttsx3.init()

voices = engine.getProperty('voices')


male_voice_index = 0 
engine.setProperty('voice', voices[male_voice_index].id)

engine.setProperty('rate', 150)  # Lower rate = slower, more deliberate
engine.setProperty('volume', 1.0)  # Max volume


JARVIS_PROMPT = (
    "You are Jarvis, a highly intelligent, polite, and professional AI assistant "
    "with a calm and friendly tone. Always respond in this style."
)

def speak(text):
    print(f"[DEBUG] Speaking: {text}")
    sentences = re.split(r'(?<=[.!?]) +', text)
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            print(f"Jarvis: {sentence}")
            engine.say(sentence)
            engine.runAndWait()
            time.sleep(0.5)  
    print()

def ask_jarvis(user_input):
    full_prompt = f"{JARVIS_PROMPT}\nUser: {user_input}\nJarvis:"
    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, there was an error: {str(e)}"

print("Jarvis is online. Ask me anything. Say 'exit' to shut down.\n")
speak("Hello there! How may I assist you today?")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "shutdown", "bye"]:
        speak("Shutting down. Goodbye.")
        break
    response = ask_jarvis(user_input)
    if response:
        speak(response)
    else:
        speak("Sorry, I did not get a response.")
    engine.stop()  # Stop engine to reset it before next input