from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

with client.messages.stream(
    model='claude-sonnet-5', 
    max_tokens=1024,
    messages=[{'role': 'user', 'content': 'Hello this is my first python with an LLM integrated, any tips?'}]
    ) as stream:
    for text in stream.text_stream:
        print(text, end='' , flush=True)



