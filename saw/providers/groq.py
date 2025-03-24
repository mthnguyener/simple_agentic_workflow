#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Groq Call Module

"""
from groq import AsyncGroq, Groq
from groq._streaming import Stream, AsyncStream
from groq.types.chat.chat_completion import ChatCompletion
from groq.types.chat.chat_completion_chunk import ChatCompletionChunk


def create_client() -> Groq:
    """
    Creates and returns a Groq client.

    Returns:
        Groq: The Groq client.
    """
    return Groq()


def generate_content(
        client: Groq,
        model: str,
        prompt: str,
        system_prompt: str,
        **params
) -> ChatCompletion | Stream[ChatCompletionChunk]:
    """
    Generates content using the Groq client.

    Args:
        client (Groq): The Groq client.
        model (str): The Groq model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Groq parameters.

    Returns:
        ChatCompletion | Stream[ChatCompletionChunk]:
            The generated content response.
    """
    return client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        model=model,
        **params
    )


async def async_generate_content(
        client: AsyncGroq,
        model: str,
        prompt: str,
        system_prompt: str,
        **params
) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
    """
    Asynchronously generates content using the Groq client.

    Args:
        client (AsyncGroq): The Groq client.
        model (str): The Groq model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Groq parameters.

    Returns:
        ChatCompletion | AsyncStream[ChatCompletionChunk]:
            The generated content response.
    """
    return await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        model=model,
        **params
    )


def groq_call(model: str, prompt: str, system_prompt: str,
              **params) -> str | None:
    """Groq LLM call function, now with params support.

    Args:
        model (str): The Groq model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Groq parameters.

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
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")
        return None


async def agroq_call(model: str, prompt: str, system_prompt: str,
                     **params) -> str | None:
    """Asynchronous Groq LLM call function, now with params support.

    Args:
        model (str): The Groq model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Groq parameters.

    Returns:
        str: The generated text, or None on error.
    """
    try:
        client = AsyncGroq()
        response = await async_generate_content(client, model, prompt,
                                                system_prompt, **params)
        print(f"Response: {response.__dict__.keys()}")
        print(f"Model: {response.model}")
        print(f"Usage: {response.usage}")
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")
        return None


if __name__ == '__main__':
    pass
