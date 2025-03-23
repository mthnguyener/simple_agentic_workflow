#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Symphonic-LLM Prompt Templates

"""

COMPOSER_PROMPT = """
{composer_prompt}

Task: {task}

Return your response in this format:

<analysis>
Based on your understanding of the task, propose a set of practical \
variations that could be implemented. For each variation, explain the \
specific problem it aims to solve or the specific improvement it aims to \
achieve, and how it differs from the original approach.
</analysis>

<tasks>
    {subtasks}
</tasks>
"""

WORKER_PROMPT = """
{worker_prompt}

Return your response in this format:

<response>
Your content here, maintaining the specified style and fully addressing \
requirements.
</response>
"""
