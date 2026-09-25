import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("NEBIUS_API_KEY")

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="nvidia/nemotron-3-super-120b-a12b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: CONNECTION SUCCESSFUL"
        }
    ],
)

print(response.choices[0].message.content)

