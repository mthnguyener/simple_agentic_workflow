#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" LLM Chaining Module

"""
from saw.core.model_interface import model_call, amodel_call
from saw.workflows.utils import apply_functions, aapply_functions


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
        processed_prompt = apply_functions(
            prompt=prompt_details["prompt"],
            functions=prompt_details["functions"]
        )
        print(f'Model: {prompt_details["provider"]}-{prompt_details["model"]}')

        print(f"\nStep {i}: {processed_prompt}")
        result = model_call(
            prompt=f"{processed_prompt}\nInput: {result}",
            provider=prompt_details["provider"],
            model=prompt_details["model"],
            system_prompt=prompt_details["system_prompt"],
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
        processed_prompt = await aapply_functions(
            prompt=prompt_details["prompt"],
            functions=prompt_details["functions"]
        )
        print(f'Model: {prompt_details["provider"]}-{prompt_details["model"]}')

        print(f"\nStep {i}: {processed_prompt}")
        result = await amodel_call(
            prompt=f"{processed_prompt}\nInput: {result}",
            provider=prompt_details["provider"],
            model=prompt_details["model"],
            system_prompt=prompt_details["system_prompt"],
            **params
        )
        print(f"\nResult: {result}")
    return result


if __name__ == '__main__':
    pass
