# Symphonic LLM
Symphonic LLM workflow is designed to handle complex tasks as well as relevant 
subtasks. This approach is inspired by the concept of a symphony, where a 
composer (conductor) directs various musicians (workers) to create a harmonious 
performance.

## Key Components
1. Composer: The composer is responsible for analyzing the main task and 
decomposing it into distinct subtasks. It uses a specific prompt to understand 
the task and generate a structured plan for the workers to follow.  
2. Workers: The workers are responsible for executing the subtasks generated 
by the composer. Each worker receives a specific subtask and generates content 
or performs actions based on the given instructions. 

## Example: Sumphonic Workflow
```Python
import asyncio

from saw.workflow import AgentWorkflow

# Initialize the AgentWorkflow for symphonic workflow
agent = AgentWorkflow(operation="symphonic")

# Define the composer and worker details
composer_details = {
    "main_task": {"task": "Write a product description for a new "
                  "high-performance running shoe"},
    "prompt": "Analyze this task and break it down into a couple of "
              "distinct approaches",
    "provider": "google",
    "model": "gemini-2.0-flash",
    "system_prompt": "You are a task composer."
}

worker_details = {
    "subtasks": [
        {"type": "technical", "description": "Write a precise, technical "
         "version that emphasizes specifications and performance metrics"},
        {"type": "lifestyle", "description": "Write an engaging, "
         "lifestyle-oriented version that connects with runners and "
         "fitness enthusiasts"}
    ],
    "prompt": "Generate content based on:\nTask: {original_task}\n"
    "Style: {task_type}\nGuidelines: {task_description}",
    "provider": "google",
    "model": "gemini-2.0-flash",
    "system_prompt": "You are a task worker."
}

# Execute the workflow
result = agent.execute(composer_details=composer_details,
                       worker_details=worker_details)

print(f"Analysis:\n{result['analysis']}")
print(f"Worker Results:\n{result['worker_results']}")

# Execute the workflow asynchronously
async def main():
    result = await agent.execute(composer_details=composer_details,
                                 worker_details=worker_details,
                                 async_mode=True)
    print(f"Analysis:\n{result['analysis']}")
    print(f"Worker Results:\n{result['worker_results']}")

asyncio.run(main())
```

## Notebook Tutorials
For more examples and detailed usage, please refer to the documentation or 
the example notebooks provided in the [notebooks](../../../notebooks) directory.
