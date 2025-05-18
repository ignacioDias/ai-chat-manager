import google.generativeai as genai
from ai_model_profile import AI_Model_Profile

class Gemini_Profile(AI_Model_Profile):
    def send_message(self, message):
        self.history.append({"role": "user", "content": message})
        genai.configure(api_key=self.api_key)
        try:
            model = genai.GenerativeModel(self.model)
            chat_history = []
            for msg in self.history:
                if msg["role"] == "user":
                    chat_history.append({"role": "user", "parts": [msg["content"]]})
                else:
                    chat_history.append({"role": "model", "parts": [msg["content"]]})
            response = model.generate_content(chat_history)
            response_message = response.text
            self.history.append({"role": "assistant", "content": response_message})
            return response_message
        except Exception as e:
            return f"Error: {str(e)}"