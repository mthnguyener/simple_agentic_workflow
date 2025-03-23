# Notebooks
This directory contains various Jupyter notebooks and scripts that demonstrate 
the usage of the `saw` library for different workflows, including 
chaining, parallelization, routing, and symphonic processing.

## Notebook Tutorials

### `agent_workflow.ipynb`
This notebook demonstrates the usage of the `AgentWorkflow` class for different 
operations such as chaining, parallelization, routing, and adaptive workflows. 
It includes both synchronous and asynchronous examples.

### `multi_llm.ipynb`
This notebook showcases the use of multiple LLMs (Large Language Models) for 
different tasks. It includes examples of chaining, parallelization, and 
routing using synchronous and asynchronous methods.

### `adaptive_llm.ipynb`
This notebook demonstrates the adaptive workflow using the AgentWorkflow class. 
It includes examples of evaluating and generating solutions iteratively, with 
a focus on code correctness, efficiency, and adherence to design patterns. 
Both synchronous and asynchronous methods are covered.

### `symphonic_llm.ipynb`
This notebook illustrates the symphonic processing workflow using the 
`Symphony` class. It includes examples of both synchronous and asynchronous 
processing for tasks that require breaking down into subtasks and generating 
content.

## Environment Setup

You will need to set up the environment variables (GOOGLE_API_KEY, etc.) in 
the `.env` file 

**Load Environment Variables**: Ensure that the environment variables are 
loaded by running the following command in your notebook or script:
```python
from dotenv import load_dotenv
load_dotenv("path-to-your-env-file.env")
```
