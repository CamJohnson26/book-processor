import os

from dotenv import load_dotenv
from ollama import Client

load_dotenv()

client = Client(
  host=os.environ.get("OLLAMA_API_ENDPOINT"),
)


def chat(prompt):
    response = client.chat(model='llama3.1', messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])
    print(response.message.content)


def embed(prompt):
    try:
        return client.embed(model='llama3.1', input=prompt).embeddings[0]
    except Exception as e:
        print('Error calculating embeddings:', e)
        raise e
