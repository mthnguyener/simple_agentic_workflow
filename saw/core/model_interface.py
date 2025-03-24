#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" LLM Interface Module

"""
from typing import Any
from .backend import provider_backends, async_provider_backends, select_backend


def model_call(
        prompt: str,
        provider: str,
        model: str = "",
        system_prompt: str = "",
        **params
) -> str:
    """
    Calls the specified LLM backend.

    Args:
        prompt (str): The input prompt.
        provider (str): The provider to use.
        model (str): The model to use.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other parameters.

    Returns:
        str: The response from the LLM backend.
    """
    select_backend(provider=provider, async_mode=False)

    if provider not in provider_backends:
        raise ValueError(f"Backend '{provider}' not registered. Please "
                         f"register '{provider}' before calling the model.")

    return provider_backends[provider](
        model, prompt, system_prompt, **params)


async def amodel_call(
        prompt: str,
        provider: str,
        model: str = "",
        system_prompt: str = "",
        **params
) -> Any:
    """
    Calls the specified asynchronous LLM backend.

    Args:
        prompt (str): The input prompt.
        provider (str): The provider to use.
        model (str): The model to use.
        system_prompt (str): The system prompt.
        params (dict): A dictionary of other parameters.

    Returns:
        str: The response from the LLM backend.
    """
    select_backend(provider=provider, async_mode=True)

    if provider not in async_provider_backends:
        raise ValueError(f"Backend '{provider}' not registered. Please "
                         f"register '{provider}' before calling the model.")

    return await async_provider_backends[provider](
        model, prompt, system_prompt, **params)


if __name__ == '__main__':
    pass
