#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" LLM Routing Module

"""
from saw.core.model_interface import model_call, amodel_call
from saw.core.processor import extract_xml
from saw.workflows.multi_llm.templates import SELECTOR_TEMPLATE
from saw.workflows.utils import apply_functions


def route(
        query: dict,
        reasoning_prompt: str,
        route_prompt: str,
        routes: dict[str, dict],
        **params: dict
) -> str:
    """Routes a query to the most appropriate model call based on the content.

    Args:
        query (dict): The input query details.
        reasoning_prompt (str): The template for the reasoning prompt.
        route_prompt (str): The template for the route prompt.
        routes (dict[str, dict]): A dictionary mapping route keys to
            dictionaries containing prompt details.
        params (dict): A dictionary of other parameters.

    Returns:
        str: The response from the selected support team.
    """
    print(f"\nAvailable routes: {list(routes.keys())}")

    selector_prompt = SELECTOR_TEMPLATE.format(
        routes=list(routes.keys()),
        route_prompt=route_prompt,
        reasoning_prompt=reasoning_prompt,
        query=query["prompt"]
    )

    query_details = apply_functions(prompt_details=query)
    route_response = model_call(prompt=selector_prompt,
                                provider=query_details.provider,
                                model=query_details.model,
                                system_prompt=query_details.system_prompt,
                                **params)
    reasoning = extract_xml(route_response, "reasoning")
    selection = extract_xml(route_response, "selection").strip().lower()

    print("\nRouting Analysis:")
    print(f"Reasoning: {reasoning}")
    print(f"Selection: {selection}")

    # Process query with selected specialized prompt
    selected_prompt_details = routes[selection]
    processed_details = apply_functions(prompt_details=selected_prompt_details)
    print(f"Model: {processed_details.provider}-{processed_details.model}")

    result = model_call(
        prompt=f"{processed_details.prompt}\nQuery: {query["prompt"]}",
        provider=processed_details.provider,
        model=processed_details.model,
        system_prompt=processed_details.system_prompt,
        **params
    )
    print(f"Result: {result}")
    return result


async def aroute(
        query: dict,
        reasoning_prompt: str,
        route_prompt: str,
        routes: dict[str, dict],
        **params: dict
) -> str:
    """Asynchronously routes a query to the most appropriate model call.

    Args:
        query (dict): The input query details.
        reasoning_prompt (str): The template for the reasoning prompt.
        route_prompt (str): The template for the route prompt.
        routes (dict[str, dict]): A dictionary mapping route keys to
            prompt details.
        params (dict): A dictionary of other parameters.

    Returns:
        str: The response from the selected support team.
    """
    print(f"\nAvailable routes: {list(routes.keys())}")

    selector_prompt = SELECTOR_TEMPLATE.format(
        routes=list(routes.keys()),
        route_prompt=route_prompt,
        reasoning_prompt=reasoning_prompt,
        query=query["prompt"]
    )

    query_details = apply_functions(prompt_details=query)
    route_response = await amodel_call(prompt=selector_prompt,
                                provider=query_details.provider,
                                model=query_details.model,
                                system_prompt=query_details.system_prompt,
                                **params)

    reasoning = extract_xml(route_response, "reasoning")
    selection = extract_xml(route_response, "selection").strip().lower()

    print("\nRouting Analysis:")
    print(f"Reasoning: {reasoning}")
    print(f"Selection: {selection}")

    # Process query with selected specialized prompt
    selected_prompt_details = routes[selection]
    processed_details = apply_functions(prompt_details=selected_prompt_details)
    print(f"Model: {processed_details.provider}-{processed_details.model}")

    result = await amodel_call(
        prompt=f"{processed_details.prompt}\nQuery: {query["prompt"]}",
        provider=processed_details.provider,
        model=processed_details.model,
        system_prompt=processed_details.system_prompt,
        **params
    )
    print(f"Result: {result}")
    return result

if __name__ == '__main__':
    pass
