#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Ollama Call Module

"""
import ollama


def ollama_pull(model: str):
    """
    Pulls the specified Ollama model.

    Args:
        model (str): The Ollama model name.
    """
    try:
        list_response: ollama.ListResponse = ollama.list()
        model_list = [m.model for m in list_response.models]
        if model not in model_list:
            print(f"Model {model} not found. Pulling model...")
            response = ollama.pull(model, stream=True)
            progress_states = set()
            for progress in response:
                if progress.get('status') in progress_states:
                    continue
                progress_states.add(progress.get('status'))
                print(progress.get('status'))
            print(f"Updated Model List: {ollama.list().models[0].model}")
    except Exception as e:
        print(f"Unable to pull {model} from Ollama. {e}")


def generate_response(model: str, prompt: str, system_prompt: str,
                      **params) -> ollama.GenerateResponse:
    """
    Generates a response from the Ollama model.

    Args:
        model (str): The Ollama model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Ollama parameters.

    Returns:
        ollama.GenerateResponse: The generated response.
    """
    return ollama.generate(
        model=model,
        prompt=prompt,
        system=system_prompt if system_prompt
        else "You are a helpful assistant.",
        options=params
    )


async def async_generate_response(model: str, prompt: str, system_prompt: str,
                                  **params) -> ollama.GenerateResponse:
    """
    Asynchronously generates a response from the Ollama model.

    Args:
        model (str): The Ollama model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Ollama parameters.

    Returns:
        ollama.GenerateResponse: The generated response.
    """
    async_client = ollama.AsyncClient()  # Create an instance of AsyncClient
    return await async_client.generate(
        model=model,
        prompt=prompt,
        system=system_prompt if system_prompt
        else "You are a helpful assistant.",
        options=params
    )


def ollama_call(model: str, prompt: str, system_prompt: str,
                **params) -> str | None:
    """Ollama LLM call function, now with params support.

    Args:
        model (str): The Ollama model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Ollama parameters.

    Returns:
        str: The generated text, or None on error.
    """
    try:
        ollama_pull(model)
        response = generate_response(model, prompt, system_prompt, **params)
        print(f"Response: {response.__dict__.keys()}")
        print(f"Using model: {response['model']}")
        return response.response
    except Exception as e:
        print(f"Ollama Error: {e}")
        return None


async def aollama_call(model: str, prompt: str, system_prompt: str,
                       **params) -> str | None:
    """Asynchronous Ollama LLM call function, now with params support.

    Args:
        model (str): The Ollama model name.
        prompt (str): The user's prompt.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other Ollama parameters.

    Returns:
        str: The generated text, or None on error.
    """
    try:
        ollama_pull(model)
        response = await async_generate_response(model, prompt,
                                                 system_prompt, **params)
        print(f"Response: {response.__dict__.keys()}")
        print(f"Using model: {response['model']}")
        return response.response
    except Exception as e:
        print(f"Ollama Error: {e}")
        return None


if __name__ == '__main__':
    pass
