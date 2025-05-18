from abc import ABC, abstractmethod

class AI_Model_Profile(ABC):
    def __init__(self, name, api_key, model):
        self.name = name
        self.api_key = api_key
        self.history = []
        self.model = model

    @abstractmethod
    def send_message(self, message):
        pass