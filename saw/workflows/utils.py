#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Workflow Utilities Module

"""
from typing import Any, Callable, Dict, List, Optional, Union


def apply_functions(prompt: str, functions: List[Callable],
                    **kwargs) -> str:
    """Apply a list of functions to a prompt.

    Args:
        prompt (str): The input prompt.
        functions (List[Callable]): A list of async functions to apply.
        kwargs (dict): Additional parameters to pass to the functions.

    Returns:
        str: The processed prompt.
    """
    for func in functions:
        prompt = func(prompt, **kwargs)

    return prompt


async def aapply_functions(prompt: str, functions: List[Callable],
                           **kwargs) -> str:
    """Apply a list of async functions to a prompt.

    Args:
        prompt (str): The input prompt.
        functions (List[Callable]): A list of async functions to apply.
        kwargs (dict): Additional parameters to pass to the functions.

    Returns:
        str: The processed prompt.
    """
    for func in functions:
        prompt = await func(prompt, **kwargs)

    return prompt


def build_func_args(
        custom_workflow: Any,
        prompts: Optional[Union[dict, List[Dict[str, Any]]]],
        query: Union[Dict, str],
        reasoning_prompt: str,
        route_prompt: str,
        routes: Optional[Dict[str, Dict[str, Any]]],
        params: Dict[str, Any]
) -> Dict[str, Any]:
    """Build function arguments for a custom workflow.

    Args:
        custom_workflow (Any): The custom workflow function.
        prompts (Optional[Union[dict, List[Dict[str, Any]]]]):
            Prompts for chaining.
        query (Union[Dict, str]): The input query.
        reasoning_prompt (str): The template for the reasoning prompt.
        route_prompt (str): The template for the route prompt.
        routes (Optional[Dict[str, Dict[str, Any]]]): Routes for routing.
        params (Dict[str, Any]): Additional parameters.

    Returns:
        Dict[str, Any]: The function arguments.
    """
    func_args = {}
    for key in custom_workflow.__annotations__.keys():
        if key == "prompts":
            func_args[key] = prompts
        elif key == "query":
            func_args[key] = query
        elif key == "reasoning_prompt":
            func_args[key] = reasoning_prompt
        elif key == "route_prompt":
            func_args[key] = route_prompt
        elif key == "routes":
            func_args[key] = routes
        elif key != "return" and key in params:
            func_args[key] = params[key]
    print(f"Function Arguments: {func_args}")
    return func_args
