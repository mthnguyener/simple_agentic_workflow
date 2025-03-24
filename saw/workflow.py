#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Agent Workflow Module

"""
from typing import Any, Callable, Dict, List, Optional, Union

from saw.workflows.adaptive_llm.adaptive import adaptive, aadaptive
from saw.workflows.multi_llm.chaining import chain, achain
from saw.workflows.multi_llm.parallelization import parallel, aparallel
from saw.workflows.multi_llm.routing import route, aroute
from saw.workflows.symphonic_llm.symphonic import symphony, asymphony
from saw.workflows.utils import build_func_args


class AgentWorkflow:
    def __init__(self, operation: str,
                 custom_workflow: Optional[Callable] = None):
        """
        Initializes an AgentWorkflow.

        Attributes:
            operation (str): The operation to perform.
            custom_workflow (Optional[Callable]): A custom workflow to execute.
        """
        self.operation = operation
        self.custom_workflow = custom_workflow

    def _execute_workflow(
            self,
            query: Union[Dict, str] = None,
            prompts: Optional[Union[dict, List[Dict[str, Any]]]] = None,
            reasoning_prompt: str = None,
            route_prompt: str = None,
            routes: Optional[Dict[str, Dict[str, Any]]] = None,
            n_workers: int = 3,
            **params: Dict[str, Any]
    ) -> Union[Dict, str, List[tuple[str, Any]], tuple[str, list[dict]]]:
        """
        Execute the specified workflow synchronously.

        Args:
            query (dict | str): The input query.
            prompts (Optional[Union[dict, List[Dict[str, Any]]]]):
                Prompts for chaining.
            reasoning_prompt (str): The template for the reasoning prompt.
            route_prompt (str): The template for the route prompt.
            routes (Optional[Dict[str, Dict[str, Any]]]): Routes for routing.
            n_workers (int): The number of workers to use for parallelization.
            params (Dict[str, Any]): Additional parameters.

        Returns:
            Union[Dict, str, List[tuple[str, Any]], tuple[str, list[dict]]]:
                The result of the operation.
        """
        if self.operation == "custom" and self.custom_workflow:
            func_args = build_func_args(self.custom_workflow, prompts, query,
                                        reasoning_prompt, route_prompt, routes,
                                        params)
            return self.custom_workflow(**func_args)
        elif self.operation == "chaining":
            return chain(query=query, prompts=prompts, **params)
        elif self.operation == "parallelization":
            return parallel(query=query, prompts=prompts,
                            n_workers=n_workers, **params)
        elif self.operation == "routing":
            return route(prompt=prompts, reasoning_prompt=reasoning_prompt,
                         route_prompt=route_prompt, routes=routes, **params)
        elif self.operation == "adaptive":
            return adaptive(
                evaluator_prompt_details=params.get("evaluator_prompt", ""),
                generator_prompt_details=params.get("generator_prompt", ""),
                ratings=params.get("ratings", []),
                task=params.get("task", ""),
                max_iterations=params.get("max_iterations", None)
            )
        elif self.operation == "symphonic":
            return symphony(
                composer_details=params.get("composer_details", {}),
                worker_details=params.get("worker_details", {})
            )
        else:
            raise ValueError(f"Unknown operation: {self.operation}")

    async def _aexecute_workflow(
            self,
            query: Union[Dict, str] = None,
            prompts: Optional[Union[dict, List[Dict[str, Any]]]] = None,
            reasoning_prompt: str = None,
            route_prompt: str = None,
            routes: Optional[Dict[str, Dict[str, Any]]] = None,
            **params: Dict[str, Any]
    ) -> Union[Dict, str, List[tuple[str, Any]], tuple[str, list[dict]]]:
        """
        Execute the specified workflow asynchronously.

        Args:
            query (dict | str): The input query.
            prompts (Optional[Union[dict, List[Dict[str, Any]]]]):
                Prompts for chaining.
            reasoning_prompt (str): The template for the reasoning prompt.
            route_prompt (str): The template for the route prompt.
            routes (Optional[Dict[str, Dict[str, Any]]]): Routes for routing.
            params (Dict[str, Any]): Additional parameters.

        Returns:
            Union[Dict, str, List[tuple[str, Any]], tuple[str, list[dict]]]:
                The result of the operation.
        """
        if self.operation == "custom" and self.custom_workflow:
            func_args = build_func_args(self.custom_workflow, prompts, query,
                                        reasoning_prompt, route_prompt, routes,
                                        params)
            return await self.custom_workflow(**func_args)
        elif self.operation == "chaining":
            return await achain(query=query, prompts=prompts, **params)
        elif self.operation == "parallelization":
            return await aparallel(query=query, prompts=prompts, **params)
        elif self.operation == "routing":
            return await aroute(prompt=prompts,
                                reasoning_prompt=reasoning_prompt,
                                route_prompt=route_prompt,
                                routes=routes, **params)
        elif self.operation == "adaptive":
            return await aadaptive(
                evaluator_prompt_details=params.get("evaluator_prompt", ""),
                generator_prompt_details=params.get("generator_prompt", ""),
                ratings=params.get("ratings", []),
                task=params.get("task", ""),
                max_iterations=params.get("max_iterations", None)
            )
        elif self.operation == "symphonic":
            return await asymphony(
                composer_details=params.get("composer_details", {}),
                worker_details=params.get("worker_details", {})
            )
        else:
            raise ValueError(f"Unknown operation: {self.operation}")

    def execute(
            self,
            query: Union[Dict, str] = None,
            prompts: Optional[Union[dict, List[Dict[str, Any]]]] = None,
            reasoning_prompt: str = None,
            route_prompt: str = None,
            routes: Optional[Dict[str, Dict[str, Any]]] = None,
            n_workers: int = 3,
            async_mode: bool = False,
            **params: Union[Dict[str, Any], int, list, str]
    ) -> Union[dict, str, List[tuple[str, Any]], Any]:
        """
        Execute the specified workflow.

        Args:
            async_mode (bool): Whether to execute the workflow asynchronously.
            query (dict | str): The input query.
            prompts (Optional[Union[dict, List[Dict[str, Any]]]]): \
                Prompts for chaining.
            reasoning_prompt (str): The template for the reasoning prompt.
            route_prompt (str): The template for the route prompt.
            routes (Optional[Dict[str, Dict[str, Any]]]): Routes for routing.
            n_workers (int): The number of workers to use for parallelization.
            params (Dict[str, Any]): Additional parameters.

        Returns:
            Union[str, List[tuple[str, Any]], Any]: The result of the operation.
        """
        if async_mode:
            return self._aexecute_workflow(query=query, prompts=prompts,
                                           reasoning_prompt=reasoning_prompt,
                                           route_prompt=route_prompt,
                                           routes=routes, **params)
        else:
            return self._execute_workflow(query=query, prompts=prompts,
                                          reasoning_prompt=reasoning_prompt,
                                          route_prompt=route_prompt,
                                          routes=routes, n_workers=n_workers,
                                          **params)


if __name__ == "__main__":
    pass
