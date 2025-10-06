import threading
import queue
from ai_engine import AIEngine
from tts_engine import TTSEngine
from speech_recognition import SpeechRecognizer
from gui import JarvisGUI
from utils import print_typing

class JarvisController:
    def __init__(self):
        self.ai = AIEngine()
        self.tts = TTSEngine()
        self.gui = JarvisGUI(on_user_input=self.handle_text_input)
        self.speech_recognizer = SpeechRecognizer(
            wake_word="jarvis",
            on_wake_callback=self.on_wake,
            on_speech_callback=self.handle_speech_input
        )
        self.message_queue = queue.Queue()
        self.is_processing = False

    def start(self):
        self.gui.start()
        self.speech_recognizer.start()
        self.gui.display_text("Jarvis: Hello there! How may I assist you today?")
        self.tts.synthesize_and_play("Hello there! How may I assist you today?")

    def on_wake(self):
        self.gui.display_text("Listening...")
        self.tts.synthesize_and_play("Yes, I am listening.")

    def handle_speech_input(self, text):
        self.process_input(text)

    def handle_text_input(self, text):
        self.process_input(text)

    def process_input(self, text):
        if self.is_processing:
            self.message_queue.put(text)
            return

        self.is_processing = True
        threading.Thread(target=self._process_input_thread, args=(text,), daemon=True).start()

    def _process_input_thread(self, text):
        print(f"User said: {text}")
        sentences = self.ai.ask(text)

        for sentence in sentences:
            self.gui.display_text(f"Jarvis: {sentence}")
            print_typing(f"Jarvis: {sentence}")
            self.tts.synthesize_and_play(sentence)
            # Wait roughly for TTS to finish speaking before continuing
            import time
            time.sleep(max(1.5, len(sentence)*0.06))

        self.is_processing = False
        # Process next queued message if any
        if not self.message_queue.empty():
            next_text = self.message_queue.get()
            self.process_input(next_text)

if __name__ == "__main__":
    controller = JarvisController()
    controller.start()

    # Keep the main thread alive while daemon threads run
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down Jarvis...")
