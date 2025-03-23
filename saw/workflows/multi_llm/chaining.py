#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" LLM Chaining Module

"""
from saw.core.model_interface import model_call, amodel_call
from saw.workflows.utils import apply_functions


def chain(
        query: str,
        prompts: list[dict],
        **params: dict
) -> str:
    """Chains multiple prompts together to process a query.

    Args:
        query (str): The input query.
        prompts (list[dict]): A list of dictionaries containing prompt details.
        params (dict): A dictionary of other parameters.

    Returns:
        str: The processed query.
    """
    result = query
    for i, prompt_details in enumerate(prompts, 1):
        processed_details = apply_functions(prompt_details=prompt_details)
        print(f"Model: {processed_details.provider}-{processed_details.model}")

        print(f"\nStep {i}: {processed_details.prompt}")
        result = model_call(
            prompt=f"{processed_details.prompt}\nInput: {result}",
            provider=processed_details.provider,
            model=processed_details.model,
            system_prompt=processed_details.system_prompt,
            **params
        )
        print(f"\nResult: {result}")
    return result

async def achain(
        query: str,
        prompts: list[dict],
        **params: dict
) -> str:
    """Asynchronous chain multiple prompts together to process a query.

    Args:
        query (str): The input query.
        prompts (list[dict]): A list of dictionaries containing prompt details.
        params (dict): A dictionary of other parameters.

    Returns:
        str: The processed query.
    """
    result = query
    for i, prompt_details in enumerate(prompts, 1):
        processed_details = apply_functions(prompt_details=prompt_details)
        print(f"Model: {processed_details.provider}-{processed_details.model}")

        print(f"\nStep {i}: {processed_details.prompt}")
        result = await amodel_call(
            prompt=f"{processed_details.prompt}\nInput: {result}",
            provider=processed_details.provider,
            model=processed_details.model,
            system_prompt=processed_details.system_prompt,
            **params
        )
        print(f"\nResult: {result}")
    return result


if __name__ == '__main__':
    pass
