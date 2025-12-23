#!/usr/bin/env python
# -*- coding: utf-8 -*-
from groq_helper import GroqClient

models = GroqClient.get_available_models()
print("Available Groq models:")
for model in models:
    print(f"- {model['name']}: {model['description']}")
