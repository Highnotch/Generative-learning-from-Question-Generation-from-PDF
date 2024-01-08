import openai
from user_feedback import collect_user_feedback
from quality_assurance import integrate_user_feedback
import numpy as np
from PyPDF2 import PdfFileReader
import openai

# Sujith's API_key=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
openai.api_key = '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'

import PyPDF2

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    return text


pdf_text = read_pdf('/Volumes/Personal/Projects/Py_question_generator/Python_lite.pdf')



def process_user_feedback(feedback_list, questions_list):
    for feedback in feedback_list:
        question_id = feedback.get("question_id")
        comment = feedback.get("comment")

        # Find the question with the corresponding question_id in the questions_list
        for question in questions_list:
            if question.get("question_id") == question_id:
                # Update the question with user feedback
                question["user_comment"] = comment

    return questions_list


## WE CAN CREATE CHUNKS OF CONTENT AS OPENAI API WONT ALLOW TO TAKE MORE THAN 4097 TOKENS AT A TIME

def generate_questions(content, question_ids=None):
    
    prompt = (
        "Generate 20 diverse types of Python-related questions with 4 options each. "
        "Include only one correct answer for each question. "
        "Ensure that questions are conceptual and logical, covering various Python programming topics. "
        "For each question, provide the question text, 4 answer options (A, B, C, D), "
        "and the correct answer. Also, include metadata such as difficulty level and relevant chapter or topic. "
        "Use the following text as context:\n"
        f"{content}\n"
    )

    # Using openai.Completion.create with explicit engine
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1400,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the generated questions from the response
    questions_list = []

    if 'choices' in response and response['choices']:
        choice = response['choices'][0]
        if 'text' in choice:
            content = choice['text']
            content_lines = content.split('\n')

            # Parse each question, options, and answer
            current_question = {}
            for line in content_lines:
                line = line.strip()
                if line.startswith('Answer:'):
                    # Add the correct answer to the current question
                    current_question['answer'] = line.replace('Answer:', '').strip()
                    # Extract metadata (difficulty level and chapter)
                    metadata_lines = content_lines[content_lines.index(line) + 1:]

                    # Reset metadata values
                    current_question['difficulty'] = None
                    current_question['topic'] = None

                    for metadata_line in metadata_lines:
                        if metadata_line.startswith('Difficulty level:'):
                            current_question['difficulty'] = metadata_line.replace('Difficulty level:', '').strip()
                        elif metadata_line.startswith('Relevant topic:'):
                            current_question['topic'] = metadata_line.replace('Relevant topic:', '').strip()
                            break  # Assume chapter information is the last metadata

                    # Add the current question to the questions list
                    questions_list.append(current_question.copy())  # Use a copy to avoid reference issues
                    # Reset the current question dictionary
                    current_question.clear()

                elif line:
                    # If the line is not empty, it's part of the question or options
                    if 'question' not in current_question:
                        # The first non-empty line is the question
                        current_question['question'] = line
                    else:
                        # Subsequent non-empty lines are options
                        current_question.setdefault('options', []).append(line)

            #for i, question in enumerate(questions_list):
            #    question['question'] = f"Generated Question {i + 1}"
            #    question['options'] = ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"]

            #    question['question_id'] = question_ids[i] if question_ids and i < len(question_ids) else None

    return questions_list