import openai
from .ai_model_profile import AI_Model_Profile

class GPT_Profile(AI_Model_Profile):

    def send_message(self, message):
        self.history.append({"role": "user", "content": message})
        client = openai.OpenAI(api_key=self.api_key)
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=self.history
            )
            response_message = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": response_message})
            return response_message
        except Exception as e:
            return f"Error: {str(e)}"