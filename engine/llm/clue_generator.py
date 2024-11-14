"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def get_llm_response(across_words, down_words):
    config = create_generation_config(across_words, down_words)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=config,
        system_instruction="You are a crossword clue generator who will make a unique clue for each across and down word that is provided. Make the clues creative and reference pop culture or history if possible.",
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(create_prompt(across_words, down_words))

    return response.text


def create_prompt(across_words, down_words):
    across_formatted = ", ".join(f"'{word}'" for word in across_words)
    down_formatted = ", ".join(f"'{word}'" for word in down_words)

    return f"Across: {across_formatted}, Down: {down_formatted}"


def create_generation_config(across_words, down_words):
    across_properties = {word: {"type": "string"} for word in across_words}

    down_properties = {word: {"type": "string"} for word in down_words}

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_schema": {
            "type": "object",
            "enum": [],
            "required": ["across_clues", "down_clues"],
            "properties": {
                "across_clues": {
                    "type": "object",
                    "enum": [],
                    "required": across_words,
                    "properties": across_properties,
                },
                "down_clues": {
                    "type": "object",
                    "enum": [],
                    "required": down_words,
                    "properties": down_properties,
                },
            },
        },
        "response_mime_type": "application/json",
    }

    return generation_config
