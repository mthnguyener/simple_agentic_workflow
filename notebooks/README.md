# Notebooks
This directory contains various Jupyter notebooks and scripts that demonstrate
the usage of the `saw` library for different workflows, including
chaining, parallelization, routing, and symphonic processing.

## Notebook Tutorials

### [`agent_workflow.ipynb`](./agent_workflow.ipynb)
This notebook demonstrates the usage of the `AgentWorkflow` class for different
operations such as chaining, parallelization, routing, and adaptive workflows.
It includes both synchronous and asynchronous examples.

### [`multi_llm.ipynb`](./multi_llm.ipynb)
This notebook showcases the use of multiple LLMs (Large Language Models) for
different tasks. It includes examples of chaining, parallelization, and
routing using synchronous and asynchronous methods.

### [`adaptive_llm.ipynb`](./adaptive_llm.ipynb)
This notebook demonstrates the adaptive workflow focusing on feedback and evaluation.
It includes examples of evaluating and generating solutions iteratively, with
a focus on code correctness, efficiency, and adherence to design patterns.
Both synchronous and asynchronous methods are covered.

### [`symphonic_llm.ipynb`](./symphonic_llm.ipynb)
This notebook illustrates the symphonic processing workflow with a composer 
guiding workers. It includes examples of both synchronous and asynchronous
processing for tasks that require breaking down into subtasks and generating
content.

### [`custom_researcher.ipynb`](./custom_researcher.ipynb)
This notebook demonstrates the usage of custom research workflow for researching 
complex topics by scraping web content and providing detailed reports. It 
includes examples of how to set up and execute custom research tasks.

### [`custom_reviewer.ipynb`](./custom_reviewer.ipynb)
This notebook showcases the use of custom review workflow for reviewing a 
product using multiple personas and compiling a holistic product review. It 
includes examples of how to set up and perform custom reviews on various tasks.

## Environment Setup

You will need to set up the environment variables (GOOGLE_API_KEY, 
GROQ_API_KEY, OPENAI_API_KEY, etc.) in the `.env` file or use `os.environ`.

**Load Environment Variables**: Ensure that the environment variables are
loaded by running the following command in your notebook or script:
```python
from dotenv import load_dotenv
load_dotenv("path-to-your-env-file.env")
```