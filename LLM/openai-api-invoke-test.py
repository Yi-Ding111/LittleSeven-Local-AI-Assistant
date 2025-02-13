from openai import OpenAI
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()
open_api=os.getenv('OPENAI_API')
# print(open_api)

client = OpenAI(
  api_key=open_api
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
