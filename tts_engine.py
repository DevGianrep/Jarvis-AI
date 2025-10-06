import os
import threading
import wave
import tempfile
from playsound import playsound
from google import genai
from google.genai import types

class TTSEngine:
    def __init__(self, api_key="AIzaSyBLESC0RMLk5RKPg3aSeqCVZd1NEWAMj7A"):
        if not api_key:
            raise ValueError("API key must be provided")
        os.environ["GOOGLE_API_KEY"] = api_key  # If required by library
        self.client = genai.Client()
        self.lock = threading.Lock()

    def wave_file(self, filename, pcm, channels=1, rate=24000, sample_width=2):
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)

    def synthesize_and_play(self, text):
        thread = threading.Thread(target=self._play_tts, args=(text,), daemon=True)
        thread.start()

    def _play_tts(self, text):
        with self.lock:
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents=text,
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                                speaker_voice_configs=[
                                    types.SpeakerVoiceConfig(
                                        speaker='Jarvis',
                                        voice_config=types.VoiceConfig(
                                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                                voice_name='Kore',  # Male voice name example
                                            )
                                        )
                                    )
                                ]
                            )
                        )
                    )
                )
                data = response.candidates[0].content.parts[0].inline_data.data
                # data is bytes PCM audio

                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    self.wave_file(f.name, data)
                    temp_path = f.name

                playsound(temp_path)
                os.remove(temp_path)

            except Exception as e:
                print(f"[ERROR] TTS playback failed: {e}")
