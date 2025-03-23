#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" LLM Parallelization Module

"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from saw.core.model_interface import model_call, amodel_call
from saw.workflows.utils import apply_functions


def parallel(query: str,
             prompts: list[dict],
             n_workers: int = 3,
             **params: dict) -> list[tuple[str, Any]]:
    """Parallelizes the processing of multiple inputs.

    Args:
        query (str): The input query.
        prompts (list[dict]): A list of dictionaries containing prompt details.
        n_workers (int): The number of workers to use.
        params (dict): A dictionary of other parameters.

    Returns:
        list[tuple[str, Any]]: A list of processed outputs.
    """
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        futures = [
            executor.submit(
                model_call,
                f"{apply_functions(prompt_details=x).prompt}\nInput: {query}",
                apply_functions(prompt_details=x).provider,
                apply_functions(prompt_details=x).model,
                apply_functions(prompt_details=x).system_prompt,
                **params
            ) for x in prompts
        ]
        results = [
            (apply_functions(prompt_details=prompts[i]).prompt, f.result())
            for i, f in enumerate(futures)
        ]

        for inp, result in results:
            print(f"\nInput: {inp}")
            print(f"Result: {result}")

        return results


async def aparallel(query: str,
                    prompts: list[dict],
                    **params: dict) -> list[tuple[str, Any]]:
    """Asynchronously parallelizes the processing of multiple inputs.

    Args:
        query (str): The input query.
        prompts (list[dict]): A list of dictionaries containing prompt details.
        params (dict): A dictionary of other parameters.

    Returns:
        list[tuple[str, Any]]: A list of processed outputs.
    """
    tasks = [
        asyncio.create_task(
            amodel_call(
                f"{apply_functions(prompt_details=x).prompt}\nInput: {query}",
                apply_functions(prompt_details=x).provider,
                apply_functions(prompt_details=x).model,
                apply_functions(prompt_details=x).system_prompt,
                **params
            )
        ) for x in prompts
    ]
    results = await asyncio.gather(*tasks)
    results = [
        (apply_functions(prompt_details=prompts[i]).prompt, result)
        for i, result in enumerate(results)]

    for inp, result in results:
        print(f"\nInput: {inp}")
        print(f"Result: {result}")

    return results


if __name__ == '__main__':
    pass
