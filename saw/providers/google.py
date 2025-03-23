#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Google Call Module

"""
from google import genai
from google.genai import types


def create_client() -> genai.Client:
    """
    Creates and returns a Google genai client.

    Returns:
        genai.Client: The Google genai client.
    """
    return genai.Client()


def generate_content(
        client: genai.Client,
        model: str,
        prompt: str,
        system_prompt: str,
        **params
) -> types.GenerateContentResponse:
    """
    Generates content using the Google genai client.

    Args:
        client (genai.Client): The Google genai client.
        model (str): The Google model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Google parameters.

    Returns:
        types.GenerateContentResponse: The generated content response.
    """
    return client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt if system_prompt
            else "You are a helpful assistant.",
            **params
        ),
    )


async def async_generate_content(
        client: genai.Client,
        model: str,
        prompt: str,
        system_prompt: str,
        **params
) -> types.GenerateContentResponse:
    """
    Asynchronously generates content using the Google genai client.

    Args:
        client (genai.Client): The Google genai client.
        model (str): The Google model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Google parameters.

    Returns:
        types.GenerateContentResponse: The generated content response.
    """
    return await client.aio.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt if system_prompt
            else "You are a helpful assistant.",
            **params
        ),
    )


def gemini_call(model: str, prompt: str, system_prompt: str,
                **params) -> str | None:
    """Google LLM call function, now with params support.

    Args:
        model (str): The Google model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Google parameters.

    Returns:
        str: The generated text, or None on error.
    """
    try:
        client = create_client()
        response = generate_content(client, model, prompt,
                                    system_prompt, **params)
        print(f"Response: {response.__dict__.keys()}")
        print(f"Model: {response.model_version}")
        print(f"Usage: {response.usage_metadata}")
        return response.text
    except Exception as e:
        print(f"Google Error: {e}")
        return None


async def agemini_call(model: str, prompt: str, system_prompt: str,
                       **params) -> str | None:
    """Asynchronous Google LLM call function, now with params support.

    Args:
        model (str): The Google model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Google parameters.

    Returns:
        str: The generated text, or None on error.
    """
    try:
        client = create_client()
        response = await async_generate_content(client, model, prompt,
                                                system_prompt, **params)
        print(f"Response: {response.__dict__.keys()}")
        print(f"Model: {response.model_version}")
        print(f"Usage: {response.usage_metadata}")
        return response.text
    except Exception as e:
        print(f"Google Error: {e}")
        return None


if __name__ == '__main__':
    pass
