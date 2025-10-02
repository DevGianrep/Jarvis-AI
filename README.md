# Jarvis AI 

**Author:** Giancarlos Minyetti  
**Created:** October 1, 2025

---

## Project Overview

The Jarvis AI Helmet is a voice-interactive assistant powered by Google Gemini 2.5 Flash and local text-to-speech (TTS) using `pyttsx3`. Inspired by the calm and intelligent demeanor of Marvel's J.A.R.V.I.S., this assistant responds to questions in a professional tone and speaks its replies line by line.

---

## Features

- Voice responses using a system TTS voice (configurable)
- AI-generated responses using Google's Gemini model
- Always responds in a professional, polite tone (Jarvis-style)
- Continuous Q&A loop with printed and spoken responses
- Debug logging to monitor input/output

---

## Requirements

Install the required Python packages:

```bash
pip install -U google-generativeai pyttsx3
import google.generativeai as genai
import pyttsx3

