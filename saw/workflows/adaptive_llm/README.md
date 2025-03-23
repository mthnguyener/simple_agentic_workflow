# Adaptive LLM
Adaptive LLM workflow is designed to improve the performance of language models 
(LLMs) over time by utilizing a cycle of evaluation and feedback. This 
approach ensures that the LLM can learn from its previous outputs and 
continuously refine its responses.  

## Key Components
1. Evaluation: The LLM's performance on a given task is assessed based on 
specific criteria. This step identifies areas where the LLM's output may need 
improvement.
2. Feedback: Constructive feedback is provided based on the evaluation. This 
feedback highlights the strengths and weaknesses of the LLM's output.
3. Generation: The LLM generates a new solution based on the feedback and 
its previous performance. This step aims to address the identified weaknesses 
and improve the overall quality of the output.

## Example: Adaptive Workflow
```Python
import asyncio

from saw.workflow import AgentWorkflow

# Initialize the AgentWorkflow for adaptive workflow
agent = AgentWorkflow(operation="adaptive")

# Define the evaluator and generator prompts
evaluator_prompt = """
Evaluate the following code implementation for:
1. code correctness
2. efficiency
3. adherence to design patterns
4. pep8 compliance
"""

generator_prompt = """
Your goal is to complete the task based on the context and provide feedback \
on how you should reflect on them to improve your solution.
"""

ratings = ["PASS", "NEEDS_IMPROVEMENT", "FAIL"]

task = """
Implement a Queue with:
1. enqueue(x)
2. dequeue()
3. getFront()
All operations should be O(1).
"""

# Execute the workflow asynchronously
async def main():
    result, chain_of_thought = await agent.execute(
        evaluator_prompt=evaluator_prompt,
        generator_prompt=generator_prompt,
        ratings=ratings,
        task=task,
        max_interations=5,
        async_mode=True
    )
    print(result)
    print(chain_of_thought)

asyncio.run(main())
```

## Notebook Tutorials
For more examples and detailed usage, please refer to the documentation or 
the example notebooks provided in the [notebooks](../../../notebooks) directory.
