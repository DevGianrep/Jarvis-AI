import google.generativeai as genai

class AIEngine:
    def __init__(self, api_key="AIzaSyBLESC0RMLk5RKPg3aSeqCVZd1NEWAMj7A"):
        if not api_key:
            raise ValueError("API key must be provided")
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")

    def ask(self, prompt):
        full_prompt = (
            "You are Jarvis, a highly intelligent, polite, and professional AI assistant "
            "with a calm and friendly tone. Always respond in this style.\n"
            f"User: {prompt}\nJarvis:"
        )
        try:
            response = self.model.generate_content(full_prompt)
            text = response.text.strip()
            # Split into sentences for line-by-line reading
            sentences = [s.strip() for s in text.split('. ') if s.strip()]
            return sentences
        except Exception as e:
            return [f"Sorry, there was an error: {str(e)}"]
