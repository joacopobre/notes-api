import voyageai
import os 
from dotenv import load_dotenv

load_dotenv()

client = voyageai.Client()

result = client.embed(texts=['cat'], model='voyage-3.5')

first_emb = result.embeddings[0]
print(len(first_emb))