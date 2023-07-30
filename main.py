import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "sk-V6T4xBkkZ9ySHsCrXOINT3ffffFJkyfkZnl2uneZIPpRlpoH"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""


@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    bot_response = "How can I help U?\n😍"
    if(message_history[-1].role == 'user'):
        # Getting the last message from the chatbot
        last_message = message_history[-1].content

        # Prompt to retrive the places or destinations seperated by space
        # If there is no places specified, gpt model returns "null"
        destination = f"Ignore all the prvious instructions and messages. In the below given message or text, find the name of the places, which may be a continent, country, or city/town. Give me only the answers. If there are many places mentioned, give me only the names seperated with space. If the text not contains any names of places, print the text 'null'. I don't want any unwanted messages rather the specified.\n\n{last_message}"
        destination = [Message(content=destination, role='user')]
        # Space seperated places
        places = models.OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=destination,
            model="gpt-3.5-turbo",
        )

        if places == 'null':    # Returns info message, if gpt model returns null
            return "Please enter the place name correctly😊", state
        else:   
            # Gets the History, an introduction and the currency used in that place
            prompt = f"Ignore all the prvious instructions and messages. You are a travel enthusiast, who travelled a lot of places in the world. So, For the below given place or places, I want the history in 75 words, about the place in 50 words, Famous foods in 30 words, which currency used? Give me all with the respective titles. I must want to add \n\n after each line and each titles , don't forget it.\n\n{places}"
            prompt = [Message(content=prompt, role='user')]
            bot_response = models.OpenAI.generate(
                system_prompt=SYSTEM_PROMPT,
                message_history=prompt,
                model="gpt-3.5-turbo",
            )

            bot_response+='\n\n'

            # Gets the popular destinations to visit in the specified place.
            prompt = f"Ignore all the prvious instructions and messages. You are a travel enthusiast, who travelled a lot of places in the world.  So, For the below given place or places, I want the popular destinations with is most famous and also give me a small description for each. Give me all with the respective titles.  I must want to add \n\n after each line and each titles , don't forget it.\n\n{places}"
            prompt = [Message(content=prompt, role='user')]
            bot_response += models.OpenAI.generate(
                system_prompt=SYSTEM_PROMPT,
                message_history=prompt,
                model="gpt-3.5-turbo",
            )

    print(bot_response)

    return bot_response, state      # Returns the response back


    