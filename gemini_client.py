# app/ai/gemini_client.py

import os
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_ID = "gemini-2.5-flash"


def _generate(prompt: str, json_output: bool = False):

    if json_output:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
    else:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )

    return response.text


async def generate_text(prompt: str, json_output: bool = False):
    """
    Async wrapper so Gemini doesn't block FastAPI event loop
    """

    try:
        result = await asyncio.to_thread(_generate, prompt, json_output)
        return result

    except Exception as e:
        return f"Gemini Error: {str(e)}"