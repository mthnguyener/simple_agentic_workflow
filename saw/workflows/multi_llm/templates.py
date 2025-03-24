#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Multi-LLM Prompt Templates

"""

SELECTOR_TEMPLATE = """
{route_prompt}
Available route options: {routes}
First explain your reasoning, then provide your selection in this XML format:

<reasoning>
{reasoning_prompt}
</reasoning>

<selection>
The chosen selection from the above routes.
</selection>

Input: {prompt}
"""
