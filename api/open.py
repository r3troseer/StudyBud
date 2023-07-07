from decouple import config
import openai

openai.api_key = config("OPENAI_API_KEY")


class generate:
    def __init__(self, text):
        self.text = text

    def questgen(self):
        print(self.text)

    def summgen():
        pass


gen = generate("test").questgen()
# gen.questgen()
