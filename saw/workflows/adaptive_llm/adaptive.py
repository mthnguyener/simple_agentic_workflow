#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Adaptive LLM Module

"""
from saw.core.model_interface import model_call, amodel_call
from saw.core.processor import extract_xml
from saw.workflows.adaptive_llm.templates import (EVALUATOR_PROMPT,
                                                  GENERATOR_PROMPT, TASK)
from saw.workflows.utils import apply_functions

DEFAULT_GENERATOR_PROMPT = ("You are an expert assistant with vast knowledge. "
                            "You are given a "
                            "task and a context to improve the solution. "
                            "Your goal is to complete the task based on the "
                            "context.")
DEFAULT_EVALUATOR_PROMPT = ("Evaluate the following implementation and "
                            "solution based on criteria needed to complete "
                            "the task.")
DEFAULT_RATINGS = "MET CRITERIA, NEEDS_IMPROVEMENT, or DID NOT MEET CRITERIA"


def _compile_full_prompt(prompt: str, task: str, context: str = "") -> str:
    """
    Compile a full prompt for generating a solution.

    Args:
        prompt (str): The prompt to generate a solution.
        task (str): The task to generate a solution for.
        context (str): The context to improve the solution.

    Returns:
        str: The full prompt.
    """
    return f"{prompt}\n{context}\nTask: {task}" \
        if context else f"{prompt}\nTask: {task}"


def _compile_generator_response(generator_response: str) -> tuple[str, str]:
    """
    Process the generator response to extract thoughts and response.

    Args:
        generator_response (str): The response from the generator.

    Returns:
        tuple[str, str]: The extracted thoughts and response.
    """
    print(f"Generator Response: {generator_response}")
    thoughts = extract_xml(generator_response, "thoughts")
    response = extract_xml(generator_response, "response")
    if response is not None or response != "":
        response = generator_response.split("</thoughts>", 1)[-1].strip()
        response = response.replace("<response>", "").replace(
            "</response>", "").strip()

    print("\n=== GENERATION START ===")
    print(f"Thoughts:\n{thoughts}\n")
    print(f"Response:\n{response}")
    print("=== GENERATION END ===\n")

    return thoughts, response


def _generator(prompt_details: dict, task: str,
               context: str = "") -> tuple[str, str]:
    """
    Generate and improve a solution based on feedback.

    Args:
        prompt_details (dict): The prompt details to generate a solution.
        task (str): The task to generate a solution for.
        context (str): The context to improve the solution.

    Returns:
        tuple[str, str]: The thoughts and generated solution.
    """
    processed_details = apply_functions(prompt_details=prompt_details)
    full_prompt = _compile_full_prompt(processed_details.prompt, task, context)
    generator_response = model_call(
        prompt=full_prompt,
        provider=processed_details.provider,
        model=processed_details.model,
        system_prompt=processed_details.system_prompt
    )
    return _compile_generator_response(generator_response)


async def _agenerator(prompt_details: dict, task: str,
                      context: str = "") -> tuple[str, str]:
    """
    Asynchronously generate and improve a solution based on feedback.

    Args:
        prompt_details (dict): The prompt details to generate a solution.
        task (str): The task to generate a solution for.
        context (str): The context to improve the solution.

    Returns:
        tuple[str, str]: The thoughts and generated solution.
    """
    processed_details = apply_functions(prompt_details=prompt_details)
    full_prompt = _compile_full_prompt(processed_details.prompt, task, context)
    generator_response = await amodel_call(
        prompt=full_prompt,
        provider=processed_details.provider,
        model=processed_details.model,
        system_prompt=processed_details.system_prompt
    )
    return _compile_generator_response(generator_response)


def _evaluator(prompt_details: dict, content: str,
               task: str) -> tuple[str, str]:
    """
    Evaluate if a solution meets requirements.

    Args:
        prompt_details (dict): The prompt details to generate a solution.
        content (str): The content to evaluate.
        task (str): The task to evaluate a solution for.

    Returns:
        tuple[str, str]: The evaluation and feedback.
    """
    processed_details = apply_functions(prompt_details=prompt_details)
    full_prompt = (f"{processed_details.prompt}. "
                   f"Feedback is required so you must explain how "
                   f"the solution meets or does not meet the requirements\n"
                   f"Original task: {task}\n"
                   f"Content to evaluate: {content}")
    evaluator_response = model_call(
        prompt=full_prompt,
        provider=processed_details.provider,
        model=processed_details.model,
        system_prompt=processed_details.system_prompt
    )
    print(f"Evaluator Response: {evaluator_response}")
    evaluation = extract_xml(evaluator_response, "evaluation")
    feedback = extract_xml(evaluator_response, "feedback")

    print("\n=== EVALUATION START ===")
    print(f"Status: {evaluation}")
    print(f"Feedback: {feedback}")
    print("=== EVALUATION END ===\n")

    return evaluation, feedback


async def _aevaluator(prompt_details: dict, content: str,
                      task: str) -> tuple[str, str]:
    """
    Asynchronously evaluate if a solution meets requirements.

    Args:
        prompt_details (dict): The prompt details to generate a solution.
        content (str): The content to evaluate.
        task (str): The task to evaluate a solution for.

    Returns:
        tuple[str, str]: The evaluation and feedback.
    """
    processed_details = apply_functions(prompt_details=prompt_details)
    full_prompt = (f"{processed_details.prompt}. "
                   f"Feedback is required so you must explain how "
                   f"the solution meets or does not meet the requirements\n"
                   f"Original task: {task}\n"
                   f"Content to evaluate: {content}")
    evaluator_response = await amodel_call(
        prompt=full_prompt,
        provider=processed_details.provider,
        model=processed_details.model,
        system_prompt=processed_details.system_prompt
    )
    evaluation = extract_xml(evaluator_response, "evaluation")
    feedback = extract_xml(evaluator_response, "feedback")

    print("\n=== EVALUATION START ===")
    print(f"Status: {evaluation}")
    print(f"Feedback: {feedback}")
    print("=== EVALUATION END ===\n")

    return evaluation, feedback


def adaptive(evaluator_prompt_details: dict,
             generator_prompt_details: dict,
             ratings: list[str], task: str,
             max_interations: int = None) -> tuple[str, list[dict]]:
    """
    Keep generating and evaluating until requirements are met.

    Args:
        evaluator_prompt_details (dict): The prompt details for evaluation.
        generator_prompt_details (dict): The prompt details for generation.
        ratings (list[str]): The possible ratings for evaluation.
        task (str): The task to evaluate a solution for.
        max_interations (int): The maximum number of iterations.

    Returns:
        tuple[str, list[dict]]: The generated solution and chain of thought.
    """
    memory = []
    chain_of_thought = []
    loop_count = 0

    ratings = ", ".join(ratings) if ratings else DEFAULT_RATINGS
    evaluator_prompt_details["prompt"] = EVALUATOR_PROMPT.format(
        evaluator_prompt=evaluator_prompt_details.get(
            "prompt", DEFAULT_EVALUATOR_PROMPT),
        ratings=ratings
    )

    generator_prompt_details["prompt"] = GENERATOR_PROMPT.format(
        generator_prompt=generator_prompt_details.get(
            "prompt", DEFAULT_GENERATOR_PROMPT))

    task = TASK.format(task=task)

    thoughts, result = _generator(prompt_details=generator_prompt_details,
                                  task=task)
    memory.append(result)
    chain_of_thought.append({"thoughts": thoughts, "result": result})

    while max_interations is None or loop_count < max_interations:
        print(f"\n=== ITERATION: {loop_count + 1} ===\n")
        evaluation, feedback = _evaluator(
            prompt_details=evaluator_prompt_details, content=result, task=task)
        if evaluation == "PASS":
            return result, chain_of_thought

        context = "\n".join([
            "Previous attempts:",
            *[f"- {m}" for m in memory],
            f"\nFeedback: {feedback}"
        ])

        thoughts, result = _generator(
            prompt_details=generator_prompt_details, context=context,
            task=task)
        memory.append(result)
        chain_of_thought.append({"thoughts": thoughts, "result": result})
        loop_count += 1

    return result, chain_of_thought


async def aadaptive(evaluator_prompt_details: dict,
                    generator_prompt_details: dict,
                    ratings: list[str], task: str,
                    max_interations: int = None) -> tuple[str, list[dict]]:
    """
    Asynchronously keep generating and evaluating until requirements are met.

    Args:
        evaluator_prompt_details (dict): The prompt details for evaluation.
        generator_prompt_details (dict): The prompt details for generation.
        ratings (list[str]): The possible ratings for evaluation.
        task (str): The task to evaluate a solution for.
        max_interations (int): The maximum number of iterations.

    Returns:
        tuple[str, list[dict]]: The generated solution and chain of thought.
    """
    memory = []
    chain_of_thought = []
    loop_count = 0

    ratings = ", ".join(ratings) if ratings else DEFAULT_RATINGS
    evaluator_prompt_details["prompt"] = EVALUATOR_PROMPT.format(
        evaluator_prompt=evaluator_prompt_details.get(
            "prompt", DEFAULT_EVALUATOR_PROMPT),
        ratings=ratings
    )

    generator_prompt_details["prompt"] = GENERATOR_PROMPT.format(
        generator_prompt=generator_prompt_details.get(
            "prompt", DEFAULT_GENERATOR_PROMPT))

    task = TASK.format(task=task)

    thoughts, result = await _agenerator(
        prompt_details=generator_prompt_details, task=task)
    memory.append(result)
    chain_of_thought.append({"thoughts": thoughts, "result": result})

    while max_interations is None or loop_count < max_interations:
        print(f"\n=== ITERATION: {loop_count + 1} ===\n")
        evaluation, feedback = await _aevaluator(
            prompt_details=evaluator_prompt_details,
            content=result, task=task)
        if evaluation == "PASS":
            return result, chain_of_thought

        context = "\n".join([
            "Previous attempts:",
            *[f"- {m}" for m in memory],
            f"\nFeedback: {feedback}"
        ])

        thoughts, result = await _agenerator(
            prompt_details=generator_prompt_details,
            context=context, task=task)
        memory.append(result)
        chain_of_thought.append({"thoughts": thoughts, "result": result})
        loop_count += 1

    return result, chain_of_thought


if __name__ == '__main__':
    pass
