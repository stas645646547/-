# integrations/llm.py
import os
from openai import AsyncOpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

async def call_gpt(prompt, model="gpt-4o"):
    messages = [
        {"role": "system", "content": "Ты гениальный юрист Израиля, отвечаешь чётко, понятно, юридически точно, мультиязычно."},
        {"role": "user", "content": prompt}
    ]
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1
    )
    return response.choices[0].message.content