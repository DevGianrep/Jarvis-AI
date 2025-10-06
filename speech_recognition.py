import speech_recognition as sr
import threading

class SpeechRecognizer:
    def __init__(self, wake_word="jarvis", on_wake_callback=None, on_speech_callback=None):
        self.wake_word = wake_word.lower()
        self.on_wake_callback = on_wake_callback
        self.on_speech_callback = on_speech_callback
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self._stop_event = threading.Event()

    def start(self):
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()

    def stop(self):
        self._stop_event.set()

    def _listen_loop(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        while not self._stop_event.is_set():
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio).lower()
                # print(f"[DEBUG] Heard: {text}")

                if not self.listening and self.wake_word in text:
                    print("[INFO] Wake word detected!")
                    self.listening = True
                    if self.on_wake_callback:
                        self.on_wake_callback()
                elif self.listening:
                    if self.on_speech_callback:
                        self.on_speech_callback(text)
                    self.listening = False

            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"[ERROR] Speech recognition error: {e}")
