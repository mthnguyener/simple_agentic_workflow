#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" LLM Backend Module

"""
from typing import Any, Callable, Dict

from ..providers.google import gemini_call, agemini_call
from ..providers.groq import groq_call, agroq_call
from ..providers.ollama import ollama_call, aollama_call
from ..providers.openai import openai_call, aopenai_call


# Define a type alias for the LLM provider call function
Provider_Call_Function = Callable[
    [str, str, str, Dict[str, dict]], Any]
Async_Provider_Call_Function = Callable[
    [str, str, str, Dict[str, dict]], Any]

# Dictionary to store available LLM backends
provider_backends: Dict[str, Provider_Call_Function] = {}
async_provider_backends: Dict[str, Async_Provider_Call_Function] = {}


def register_backend(name: str, func: Provider_Call_Function):
    """
    Registers a provider backend with the interface.

    Args:
        name (str): The name of the backend.
        func (Provider_Call_Function): The provider call function.
    """
    provider_backends[name] = func


def aregister_backend(name: str, func: Async_Provider_Call_Function):
    """
    Registers an asynchronous provider backend with the interface.

    Args:
        name (str): The name of the backend.
        func (Async_Provider_Call_Function): \
            The asynchronous provider call function.
    """
    async_provider_backends[name] = func


def select_backend(provider: str, async_mode: bool = False):
    if provider == "google":
        if async_mode:
            aregister_backend("google", agemini_call)
        else:
            register_backend("google", gemini_call)

    if provider == "groq":
        if async_mode:
            aregister_backend("groq", agroq_call)
        else:
            register_backend("groq", groq_call)

    if provider == "ollama":
        if async_mode:
            aregister_backend("ollama", aollama_call)
        else:
            register_backend("ollama", ollama_call)

    if provider == "openai":
        if async_mode:
            aregister_backend("openai", aopenai_call)
        else:
            register_backend("openai", openai_call)


if __name__ == '__main__':
    pass
