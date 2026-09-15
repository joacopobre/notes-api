from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

message = client.messages.create(model='claude-sonnet-5', max_tokens=1024, messages=[{'role': 'user', 'content': 'Hello this is my first python with an LLM integrated, any tips?'}])

print(message.content[0].text)