import anthropic
from core.ai_model_profile import AI_Model_Profile

class Claude_Profile(AI_Model_Profile):

    def send_message(self, message):
        self.history.append({"role": "user", "content": message})
        client = anthropic.Anthropic(api_key=self.api_key)
        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=self.history
            )
            response_message = response.content[0].text
            self.history.append({"role": "assistant", "content": response_message})
            return response_message
        except Exception as e:
            return f"Error: {str(e)}"