# Multi-LLM Workflow
Multi-LLM workflows leverage the capabilities of multiple language models 
(LLMs) to solve complex tasks more efficiently and effectively. It includes 
three main approaches: chaining, parallelization, and routing.

## Key Components
1. Chaining involves processing a query through a sequence of prompts, 
where the output of one prompt becomes the input for the next. It allows for 
step-by-step refinement and transformation of the input, making it suitable 
for tasks that require a series of logical steps or stages.
2. Parallelization processes multiple prompts simultaneously using multiple LLMs.
It significantly reduces the time required to handle multiple tasks or inputs 
by distributing the workload across several models. This is ideal for tasks 
that can be divided into independent subtasks.
3. Routing routes a query to the most appropriate model based on the content 
of the query. It ensures that the query is handled by the most suitable model, 
improving the accuracy and relevance of the response. This is useful for tasks 
that require specialized knowledge or handling.

## Example 1: Chaining Workflow
```Python
import asyncio

from saw.workflow import AgentWorkflow

# Initialize the AgentWorkflow for chaining
agent = AgentWorkflow(operation="chaining")

# Define the query and input list
query = "Explain the process of photosynthesis."
prompts = [
    {
        "prompt": "Step 1: Light absorption",
        "model": "gemini-2.0-flash",
        "provider": "google",
        "system_prompt": "You are a helpful assistant.",
        "functions": [str.lower]
    },
    {
        "prompt": "Step 2: Water splitting",
        "model": "gemini-2.0-flash",
        "provider": "google",
        "system_prompt": "You are a helpful assistant.",
        "functions": [str.lower]
    },
    {
        "prompt": "Step 3: Oxygen release",
        "model": "gemini-2.0-flash",
        "provider": "google",
        "system_prompt": "You are a helpful assistant.",
        "functions": [str.lower]
    }
]

# Execute the workflow
result = agent.execute(query=query, prompts=prompts)
print(result)

# Execute the workflow asynchronously
async def main():
    result = await agent.execute(query=query, prompts=prompts, async_mode=True)
    print(result)

asyncio.run(main())
```

## Example 2: Parallelization Workflow
```Python
import asyncio

from saw.workflow import AgentWorkflow

# Initialize the AgentWorkflow for parallelization
agent = AgentWorkflow(operation="parallelization")

# Define the query and input list
query = "Analyze the following sentences."
prompts = [
    {
        "prompt": "Sentence 1: The quick brown fox jumps over the lazy dog.",
        "model": "gemini-2.0-flash",
        "provider": "google",
        "system_prompt": "You are a helpful assistant.",
        "functions": [str.lower]
    },
    {
        "prompt": "Sentence 2: A journey of a thousand miles begins with a single step.",
        "model": "gemini-2.0-flash",
        "provider": "google",
        "system_prompt": "You are a helpful assistant.",
        "functions": [str.lower]
    }
]

# Execute the workflow
results = agent.execute(query=query, prompts=prompts, n_workers=2)
print(results)

# Execute the workflow asynchronously
async def main():
    result = await agent.execute(query=query, prompts=prompts, n_workers=2,
                                 async_mode=True)
    print(result)

asyncio.run(main())
```

## Example 3: Routing Workflow
```Python
import asyncio
from saw.workflow import AgentWorkflow

# Initialize the AgentWorkflow for routing
agent = AgentWorkflow(operation="routing")

# Define the query, routes, and selector template
query = {
    "prompt": "How did the Industrial Revolution impact society?",
    "model": "gemini-2.0-flash",
    "provider": "google",
    "system_prompt": "You are a helpful assistant.",
    "functions": [str.lower]
}

routes = {
    "math_tutor": {
        "prompt": """
        You are a math tutor. Follow these guidelines:
        1. Always start with "Math Tutor Response:"
        2. Acknowledge the specific math topic
        3. Provide clear explanations and examples
        4. Suggest additional resources or exercises
        5. Encourage the student to ask further questions

        Maintain a supportive and encouraging tone.
        """,
        "model": "gemini-2.0-flash",
        "provider": "google",
        "system_prompt": "You are a helpful assistant.",
        "functions": [str.lower]
    },
    "science_tutor": {
        "prompt": """
        You are a science tutor. Follow these guidelines:
        1. Always start with "Science Tutor Response:"
        2. Acknowledge the specific science topic
        3. Provide clear explanations and examples
        4. Suggest additional resources or experiments
        5. Encourage the student to ask further questions

        Maintain a supportive and encouraging tone.
        """,
        "model": "deepseek-r1:1.5b",
        "provider": "ollama",
        "system_prompt": "You are a helpful assistant.",
        "functions": [str.lower]
    },
    "english_tutor": {
        "prompt": """
        You are an English tutor. Follow these guidelines:
        1. Always start with "English Tutor Response:"
        2. Acknowledge the specific English topic
        3. Provide clear explanations and examples
        4. Suggest additional resources or exercises
        5. Encourage the student to ask further questions

        Maintain a supportive and encouraging tone.
        """,
        "model": "gemini-2.0-flash",
        "provider": "google",
        "system_prompt": "You are a helpful assistant.",
        "functions": [str.lower]
    },
    "history_tutor": {
        "prompt": """
        You are a history tutor. Follow these guidelines:
        1. Always start with "History Tutor Response:"
        2. Acknowledge the specific history topic
        3. Provide clear explanations and examples
        4. Suggest additional resources or readings
        5. Encourage the student to ask further questions

        Maintain a supportive and encouraging tone.
        """,
        "model": "deepseek-r1:1.5b",
        "provider": "ollama",
        "system_prompt": "You are a helpful assistant.",
        "functions": [str.lower]
    }
}

route_prompt = "Analyze the input and select the most appropriate tutor."
reasoning_prompt = ("Brief explanation of why this question should be routed "
                    "to a specific tutor. Consider key terms, user intent, "
                    "and urgency level.")

# Execute the workflow
result = agent.execute(query=query, reasoning_prompt=reasoning_prompt,
                       route_prompt=route_prompt, routes=routes)
print(result)

# Execute the workflow asynchronously
async def main():
    result = await agent.execute(query=query,
                                 reasoning_prompt=reasoning_prompt,
                                 route_prompt=route_prompt, routes=routes,
                                 async_mode=True)
    print(result)

asyncio.run(main())
```

## Notebook Tutorials
For more examples and detailed usage, please refer to the documentation or 
the example notebooks provided in the [notebooks](../../../notebooks) directory.