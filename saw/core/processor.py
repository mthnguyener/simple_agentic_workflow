#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Output Processor Module

"""
import re
from typing import Dict, List


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text.

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag
    """
    match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
    return match.group(1) if match else ""


def parse_tasks(tasks_xml: str) -> List[Dict]:
    """
    Parse XML tasks into a list of task dictionaries.

    Args:
        tasks_xml (str): The XML tasks to parse.

    Returns:
        List[Dict]: A list of task dictionaries.
    """
    tasks = []
    task_pattern = re.compile(
        r'<task><type>(.*?)</type><description>(.*?)</description></task>',
        re.DOTALL
    )
    matches = task_pattern.findall(tasks_xml)

    for match in matches:
        task = {
            "type": match[0].strip(),
            "description": match[1].strip()
        }
        tasks.append(task)

    return tasks
