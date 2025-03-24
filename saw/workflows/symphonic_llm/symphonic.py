#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Symphonic LLM Module

"""
from typing import Any, Dict, List, Optional, Tuple

from saw.core.model_interface import model_call, amodel_call
from saw.core.processor import extract_xml, parse_tasks
from saw.workflows.symphonic_llm.templates import (COMPOSER_PROMPT,
                                                          WORKER_PROMPT)
from saw.workflows.utils import apply_functions, aapply_functions


def format_prompt(template: str, **kwargs) -> str:
    """
    Format a prompt template with variables.

    Args:
        template (str): The prompt template.
        kwargs (dict): A dictionary of variables to replace.

    Returns:
        str: The formatted prompt.
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required prompt variable: {e}")


def handle_worker_response(worker_response: str,
                           task_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle the worker response and extract the result.

    Args:
        worker_response (str): The response from the worker.
        task_info (Dict[str, Any]): The task information.

    Returns:
        Dict[str, Any]: The processed worker response.
    """
    result = extract_xml(worker_response, "response")
    if not result:
        result = worker_response

    print(f"Worker Response: {result}")

    return {
        "type": task_info["type"],
        "description": task_info["description"],
        "result": result
    }


def process_tasks(tasks: List[Dict[str, Any]],
                  context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Process each task using the worker LLM.

    Args:
        tasks (List[Dict[str, Any]]): List of task dictionaries.
        context (Dict[str, Any]): Context dictionary.

    Returns:
        List[Dict[str, Any]]: List of worker results.
    """
    worker_results = []

    for task_info in tasks:
        task_functions = []
        for s in context['tasks']:
            if task_info['type'] in s['type']:
                task_functions = s['functions']
        context['original_task'] = context['task']
        context['task_type'] = task_info['type']
        context['task_description'] = task_info['description']

        task_info["prompt"] = format_prompt(WORKER_PROMPT, **context)

        processed_prompt = apply_functions(
            prompt=task_info["prompt"],
            functions=task_functions
        )

        worker_response = model_call(
            prompt=processed_prompt,
            provider=context['provider'],
            model=context['model'],
            system_prompt=context['system_prompt']
        )

        worker_response_constructed = handle_worker_response(
            worker_response=worker_response, task_info=task_info)

        worker_results.append(worker_response_constructed)

    return worker_results


async def aprocess_tasks(tasks: List[Dict[str, Any]],
                         context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Asynchronously process each task using the worker LLM.

    Args:
        tasks (List[Dict[str, Any]]): List of task dictionaries.
        context (Dict[str, Any]): Context dictionary.

    Returns:
        List[Dict[str, Any]]: List of worker results.
    """
    worker_results = []

    for task_info in tasks:
        task_functions = []
        for s in context['tasks']:
            if task_info['type'] in s['type']:
                task_functions = s['functions']
        context['original_task'] = context['task']
        context['task_type'] = task_info['type']
        context['task_description'] = task_info['description']

        task_info["prompt"] = format_prompt(WORKER_PROMPT, **context)

        processed_prompt = await aapply_functions(
            prompt=task_info["prompt"],
            functions=task_functions
        )
        worker_response = await amodel_call(
            prompt=processed_prompt,
            provider=context['provider'],
            model=context['model'],
            system_prompt=context['system_prompt']
        )

        worker_response_constructed = handle_worker_response(
            worker_response=worker_response, task_info=task_info)

        worker_results.append(worker_response_constructed)

    return worker_results


def prepare_context(
        task: str,
        subtasks: Dict[str, str],
        context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Prepare the context dictionary.

    Args:
        task (str): The task to process.
        subtasks (Dict[str, str]): A dictionary of subtasks.
        context (Optional[Dict[str, Any]]): A dictionary of context variables.

    Returns:
        Dict[str, Any]: A dictionary of context variables.
    """
    context = context or {}
    context['task'] = task
    subtasks_str = ""
    for sub, desc in subtasks.items():
        subtasks_str += (f"<task><type>{sub}</type>"
                         f"<description>{desc}</description></task>")
    context['subtasks'] = subtasks_str
    return context


def prepare_contexts(
        main_task: str, subtasks: Dict[str, str],
        composer_details: Dict[str, Any],
        worker_details: Dict[str, Any]
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Prepare the context dictionaries for the composer and worker.

    Args:
        main_task (str): The task to process.
        subtasks (Dict[str, str]): A dictionary of subtasks.
        composer_details (Dict[str, Any]): Details for the composer task.
        worker_details (Dict[str, Any]): Details for the worker tasks.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: The composer and worker
            context dictionaries.
    """
    common_context = prepare_context(
        task=main_task,
        subtasks=subtasks
    )

    composer_context = {**common_context, **{
        "prompt": composer_details["prompt"],
        "tasks": composer_details["tasks"],
        "provider": composer_details["provider"],
        "model": composer_details["model"],
        "system_prompt": composer_details["system_prompt"],
    }}

    worker_context = {**common_context, **{
        "prompt": worker_details["prompt"],
        "tasks": worker_details["tasks"],
        "provider": worker_details["provider"],
        "model": worker_details["model"],
        "system_prompt": worker_details["system_prompt"]
    }}

    return composer_context, worker_context


def get_composer_response(context: Dict[str, Any]) -> str:
    """
    Get the composer response.

    Args:
        context (Dict[str, Any]): A dictionary of context variables.

    Returns:
        str: The composer response.
    """
    composer_input = format_prompt(COMPOSER_PROMPT, **context)
    processed_prompt = apply_functions(
        prompt=composer_input,
        functions=context['tasks']['functions']
    )
    composer_response = model_call(
        prompt=processed_prompt,
        provider=context['provider'],
        model=context['model'],
        system_prompt=context['system_prompt']
    )
    return composer_response


async def aget_composer_response(context: Dict[str, Any]) -> str:
    """
    Asynchronously get the composer response.

    Args:
        context (Dict[str, Any]): A dictionary of context variables.

    Returns:
        str: The composer response.
    """
    composer_input = format_prompt(COMPOSER_PROMPT, **context)
    processed_prompt = await apply_functions(
        prompt=composer_input,
        functions=context['tasks']['functions']
    )
    composer_response = await amodel_call(
        prompt=processed_prompt,
        provider=context['provider'],
        model=context['model'],
        system_prompt=context['system_prompt']
    )
    return composer_response


def symphony(composer_details: Dict[str, Any],
             worker_details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process task by breaking it down and running subtasks.

    Args:
        composer_details (Dict[str, Any]): Details for the composer task.
        worker_details (Dict[str, Any]): Details for the worker tasks.

    Returns:
        Dict[str, Any]: A dictionary of results.
    """
    subtasks = {subtask["type"]: subtask["description"]
                for subtask in worker_details["tasks"]}
    composer_context, worker_context = prepare_contexts(
        main_task=composer_details["tasks"]["task"],
        subtasks=subtasks,
        composer_details=composer_details,
        worker_details=worker_details
    )
    composer_response = get_composer_response(composer_context)
    analysis = extract_xml(composer_response, "analysis")
    tasks_xml = extract_xml(composer_response, "tasks")
    tasks = parse_tasks(tasks_xml)
    worker_results = process_tasks(tasks, worker_context)
    return {
        "analysis": analysis,
        "worker_results": worker_results,
    }

async def asymphony(composer_details: Dict[str, Any],
                    worker_details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Asynchronously process task by breaking it down and running subtasks.

    Args:
        composer_details (Dict[str, Any]): Details for the composer task.
        worker_details (Dict[str, Any]): Details for the worker tasks.

    Returns:
        Dict[str, Any]: A dictionary of results.
    """
    subtasks = {subtask["type"]: subtask["description"]
                for subtask in worker_details["tasks"]}
    composer_context, worker_context = prepare_contexts(
        main_task=composer_details["tasks"]["task"],
        subtasks=subtasks,
        composer_details=composer_details,
        worker_details=worker_details
    )
    composer_response = await aget_composer_response(composer_context)
    analysis = extract_xml(composer_response, "analysis")
    tasks_xml = extract_xml(composer_response, "tasks")
    tasks = parse_tasks(tasks_xml)
    worker_results = await aprocess_tasks(tasks, worker_context)
    return {
        "analysis": analysis,
        "worker_results": worker_results,
    }


if __name__ == "__main__":
    pass
