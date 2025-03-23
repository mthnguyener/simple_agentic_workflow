#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Workflow Utilities Module

"""
from dataclasses import dataclass


@dataclass
class PromptDetails:
    prompt: str
    model: str
    provider: str
    system_prompt: str


def apply_functions(prompt_details: dict) -> PromptDetails:
    """Apply a list of functions to a prompt.

    Args:
        prompt_details (dict): A dictionary containing prompt details.

    Returns:
        PromptDetails: The processed prompt details.
    """
    prompt = prompt_details.get('prompt')
    model = prompt_details.get('model')
    provider = prompt_details.get('provider')
    system_prompt = prompt_details.get('system_prompt')
    functions = prompt_details.get('functions', [])

    for func in functions:
        prompt = func(prompt)

    return PromptDetails(prompt=prompt, model=model,
                         provider=provider, system_prompt=system_prompt)
