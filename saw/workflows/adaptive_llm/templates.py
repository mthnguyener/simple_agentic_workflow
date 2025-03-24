#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Adaptive LLM Prompt Templates

"""

EVALUATOR_PROMPT = """
{evaluator_prompt}

Your sole function is to evaluate the provided task. \
Do not to attempt to solve the task or provide its solution.

Here are the ratings: {ratings}
Only output the rating that represents that all criteria are met if all \
criteria are met and you have no further suggestions for improvements.

Output your evaluation concisely in the following format.

<evaluation>{ratings}</evaluation>

<feedback>
What needs improvement and why.
</feedback>
"""

GENERATOR_PROMPT = """
{generator_prompt}

Your current task is: [user input].

In your subsequent responses, demonstrate a clear understanding of the \
feedback by [specify how to show understanding, e.g., \
'directly addressing each point,' \
'providing a revised version with explanations of changes,' \
'asking clarifying questions'].

Output your answer concisely in the following format:

<thoughts>
[Your understanding of the task and feedback and how you plan to improve here]
</thoughts>

<response>
[Your output and response for the task here]
</response>
"""

TASK = """
<user input>
{task}
</user input>
"""
