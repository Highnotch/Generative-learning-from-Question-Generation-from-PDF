import PyPDF2
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
from pdf_parser import parse_pdf
from question_generator import generate_questions
from quality_assurance import perform_quality_checks
from user_feedback import collect_user_feedback
from PyPDF2 import PdfFileReader
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile, HTTPException
import uuid
from question_generator import generate_questions, process_user_feedback
from quality_assurance import integrate_user_feedback,perform_quality_checks
import openai


app = FastAPI()


import PyPDF2

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    return text

# example usage
pdf_text = read_pdf('/Volumes/Personal/Projects/Py_question_generator/Python_lite.pdf')
## till here -----------------------------





    
    #commenting the below ones--------
##@app.post("/upload")
##async def upload_pdf(file: UploadFile = File(...)):
    # Upload PDF file and parse its content
    ##content = parse_pdf(file.file)








question_ids = [uuid.uuid4() for _ in range(20)]
questions = generate_questions(pdf_text, question_ids)

@app.get("/get_questions", response_class=HTMLResponse)
async def get_questions_html():
    # Generate questions based on parsed content
    html_content = ""
    html_content += "<h1>  Generative Learning Hub 🚀📚 </h1>"
    html_content += "<h2>  Generated Questions </h2>"


    for i, question in enumerate(questions, start=1):
        # Add styling for each question in a box with background color
        

        html_content += f"<div style='border: 1px solid #000; padding: 10px; margin-bottom: 20px; background-color: #e0e0e0;'>"

        html_content += f"<p>{i}. {question['question']}</p>"

        for j, option in enumerate(question['options'], start=97):  # ASCII code for 'a'
            html_content += f"<p>&nbsp;&nbsp;&nbsp; {option}</p>"

        html_content += f"<p>&nbsp;&nbsp;&nbsp;Answer: {question['answer']} </p>"
        html_content += f"<p>&nbsp;&nbsp;&nbsp;Difficulty: {question['difficulty']}</p>"
        html_content += f"<p>&nbsp;&nbsp;&nbsp;Topic: {question.get('topic')}</p>"

        html_content += "</div>"  # Close the box

    return HTMLResponse(content=html_content)

##### I AM ADDING THE BELOW STUFF-------------

## UNCOMMENT summarizer_feedback..., print("Summerized...,")...., print("summarized_feedback")..... ----- I did that to reduce requests per minute.
@app.post("/feedback")
async def user_feedback():
    try:
        
        # Collect user feedback and update the question generation model
        feedback_list=collect_user_feedback()
        summarized_feedback = integrate_user_feedback(questions, feedback_list)

        # Perform quality checks after integrating user feedback
        #questions_with_user_feedback = perform_quality_checks(questions_with_user_feedback)
        print("Summarized feedback is :")
        print(summarized_feedback)
        print("----------------------")
        print("Feedback: ")
        print(feedback_list)
        return JSONResponse(content={"message": "Feedback received and processed"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")
    
@app.get("/quality")
async def quality_check():
    return perform_quality_checks(questions)