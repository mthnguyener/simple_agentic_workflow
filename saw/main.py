#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Main Module

"""
from saw.core.model_interface import model_call

prompt = "What's 2+2?"
system_prompt = "You are a mathematician."

# Now, we use other_params to set temperature and seed:
other_params = {
    "temperature": 0.7,  # Adjust temperature for creativity
    "seed": 42,  # Set a seed for reproducibility (if supported by the model)
    # Add other Ollama parameters as needed here
}

print(f"========== Calling Ollama ==========")
model_name = "deepseek-r1:1.5b"
response = model_call(prompt=prompt, provider="ollama", model=model_name,
                      system_prompt=system_prompt, **other_params)

if response:
    print(f"Ollama Response: {response}")
else:
    print("Failed to get a response from the Ollama model.")

# Another example using Google Gemini
print(f"========== Calling Google Gemini ==========")
model_name = "gemini-2.0-flash"
response = model_call(prompt=prompt, provider="google", model=model_name,
                      system_prompt=system_prompt, **other_params)

if response:
    print(f"Google Response: {response}")
else:
    print("Failed to get a response from the Google model.")
