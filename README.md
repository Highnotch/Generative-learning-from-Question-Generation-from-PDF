# Generative-learning-from-Question-Generation-from-PDF
The Generative Learning Hub
# PyQuestionGenerator

**PyQuestionGenerator** is a Python web application that leverages OpenAI's GPT-3.5-turbo to generate diverse and conceptual questions with options, answers, and metadata such as difficulty level and topic. The application is designed to create logical questions from a given text input.

## Features

- Generates desired number of diverse types of questions with 4 options and a single correct answer or Fill in the blanks or True/False .
- Includes metadata such as question difficulty level and relevant chapter or topic in the answer section.
- Avoids asking questions like that doesn't make sense through reinforcement learning.
- Model is made such that it can be easily fine-tuned by user.
- Provides a clean and styled HTML output for easy readability.

## Usage

1. Run the web application using [FastAPI](https://fastapi.tiangolo.com/).
2. Access the generated questions through the `/get_questions` endpoint.
3. View questions in a formatted HTML output with options, answers, and metadata.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Highnotch/Generative-learning-from-Question-Generation-from-PDF

2. Install Dependecies:
   ```bash
   pip install -r requirements.txt

3. Run the application
   ```bash
   uvicorn main:app --reload

4.Open your browser and navigate to http://127.0.0.1:8000/get_questions to view the generated questions.

Configuration

Adjust the GPT-3.5-turbo API key in question_generator.py to your OpenAI API key.
Customize the prompt and input text for generating questions in main.py.
License

This project is licensed under the MIT License - see the LICENSE file for details.
   
