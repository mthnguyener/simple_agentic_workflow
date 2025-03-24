#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" OpenAI Call Module

"""
import openai
from openai._streaming import Stream, AsyncStream
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk


def create_client() -> openai.Client:
    """
    Creates and returns an OpenAI client.

    Returns:
        openai.Client: The OpenAI client.
    """
    return openai.Client()


def generate_content(
        client: openai.Client,
        model: str,
        prompt: str,
        system_prompt: str,
        **params
) ->  ChatCompletion | Stream[ChatCompletionChunk]:
    """
    Generates content using the OpenAI client.

    Args:
        client (openai.Client): The OpenAI client.
        model (str): The OpenAI model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other OpenAI parameters.

    Returns:
        openai.Completion: The generated content response.
    """
    return client.chat.completions.create(
        messages=[
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        model=model,
        **params
    )


async def async_generate_content(
        client: openai.Client,
        model: str,
        prompt: str,
        system_prompt: str,
        **params
) ->  ChatCompletion | AsyncStream[ChatCompletionChunk]:
    """
    Asynchronously generates content using the OpenAI client.

    Args:
        client (openai.Client): The OpenAI client.
        model (str): The OpenAI model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other OpenAI parameters.

    Returns:
        openai.Completion: The generated content response.
    """
    return await client.chat.completions.create(
        messages=[
            {"role": "developer", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        model=model,
        **params
    )


def openai_call(model: str, prompt: str, system_prompt: str,
                **params) -> str | None:
    """OpenAI LLM call function, now with params support.

    Args:
        model (str): The OpenAI model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other OpenAI parameters.

    Returns:
        str: The generated text, or None on error.
    """
    try:
        client = create_client()
        response = generate_content(client, model, prompt,
                                    system_prompt, **params)
        print(f"Response: {response.__dict__.keys()}")
        print(f"Model: {response.model}")
        print(f"Usage: {response.usage}")
        return response.choices[0].text
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return None


async def aopenai_call(model: str, prompt: str, system_prompt: str,
                       **params) -> str | None:
    """Asynchronous OpenAI LLM call function, now with params support.

    Args:
        model (str): The OpenAI model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other OpenAI parameters.

    Returns:
        str: The generated text, or None on error.
    """
    try:
        client = create_client()
        response = await async_generate_content(client, model, prompt,
                                                system_prompt, **params)
        print(f"Response: {response.__dict__.keys()}")
        print(f"Model: {response.model}")
        print(f"Usage: {response.usage}")
        return response.choices[0].text
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return None


if __name__ == '__main__':
    pass
