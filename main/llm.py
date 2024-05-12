import os
from groq import Groq
import dotenv
import re
import ollama
from main.memory import talking_log
dotenv.load_dotenv()
class Robot:
    """
    Represents an AI robot that can chat with users.
    Robot.groq : Groq client used for making API requests.
    ollama.ollama : Ollama client used for making API requests.

    Attributes:
    - client: The Groq client used for making API requests.
    - history: A list of chat history containing user and assistant messages.
    """

    def __init__(self,memory_path='log.json'):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.memory = talking_log(memory_path)
        self.history = self.memory.get_log()

    def gorq(self, messages):
        if self.history == []:
            self.history = [
                {
                "role": "system",
                "content": "you have to role play and talk to users as his little step sister \nYou can answer in Thai and English, but your user are Thai. You should answer in Thai only."
                },
                {
                    "role": "user",
                    "content": messages,
                }
            ]
        else:
            self.memory.write_log(speaker="user",content=messages)
            self.history = self.memory.get_log()
        result = self.client.chat.completions.create(
            messages=self.history,
            model="llama3-70b-8192",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
            seed=1,
        )
        result = result.choices[0].message.content
        self.memory.write_log(speaker="assistant",content=result)
        return result

    def ollama(self, messages):
        """
        Simulates a chat conversation between the user and the Ollama model.

        Parameters:
        - messages: A string representing the user's messages.

        Returns:
        - response: A string representing the Ollama model's response.
        """
        if self.history == []:
            self.history = [
                {
                "role": "system",
                "content": """You can answer in Thai and English, but your users are Thai. You should answer in Thai only and English if the user wants English""",
                },
                {
                    "role": "user",
                    "content": messages,
                }
            ]
        else:
            self.history.append({"role": "user", "content": messages})
        response = ollama.chat(model='llama3:8b-instruct-q5_K_S', messages=self.history)
        return response['message']['content']

    def clean_message(self, msg):
        """
        Cleans a message by removing emojis and whitespace.

        Parameters:
        - msg: A string representing the message to be cleaned.

        Returns:
        - cleaned_msg: A string representing the cleaned message.
        """
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002500-\U00002BEF"  # chinese char
                                u"\U00002702-\U000027B0"
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u"\U00010000-\U0010ffff"
                                u"\u2640-\u2642"
                                u"\u2600-\u2B55"
                                u"\u200d"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\ufe0f"  # dingbats
                                u"\u3030"
                                "]+", flags=re.UNICODE)
        cleaned_msg = emoji_pattern.sub(r'', msg)
        cleaned_msg = cleaned_msg.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return cleaned_msg


