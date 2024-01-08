import openai

def perform_quality_checks(questions):
    # Implement quality assurance checks

    for question in questions:
        # Example quality check: Ensure each question has options
        if 'options' not in question or len(question['options']) != 4: ############ CHECKS THE FORAmATE OF options
            question['error'] = "Invalid question format: Missing options or incorrect number of options"
            #return question["options"]
            return "oopsiess " + str(question) + " has " + str(question['error'])

        
        answer=question["answer"]
        answer=answer.split("a")

        # Quality check: Ensure the correct answer is one of the options
        if 'answer' not in question or question['answer']not in question['options']:
            question['error'] = "Invalid answer: Answer must be one of the provided options"
            return "oopsiess " + str(question) + " has " + str(question['error'])

        # Add more quality checks as needed
        if 'text' in question and len(question['text']) < 10:
            question['error'] = "Question text is too short, make it more elaborate"
            return "oopsiess " + str(question) + " has " + str(question['error'])
        
        unique_options = set(question.get('options', []))
        if len(unique_options) < 4:
            question['error'] = "Options should be diverse, avoid duplicates"
            return "oopsiess " + str(question) + " has " + str(question['error'])
        
# OpenAI to check for coherence in question and answer ----------- Due to RPM and RPD limit unable to process: ++
        
        coherence_prompt = f"Question: {question['question']}\nAnswer: {question['answer']},you need to just output the value of  coherence score from 1 to 10, that means the output must just be a number."
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=coherence_prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        coherence_score = response['choices'][0]['text']
        numerical_score_str = coherence_score.split('.')[0].strip()

# Converting the numerical score to an integer
        numerical_score = float(numerical_score_str)

        if float(numerical_score) < 4:
            question['error'] = "Low coherence between question and answer"
            return "oopsiess " + str(question) + " has " + str(question['error'])

#         We can Add more creative quality checks as needed


    return "All Questions have passed quality checks...YAYYYY!!!"


    #return questions
########### USING OPEN AI SUMMARIZATION TO CHANGE THE PROMPT FROM THE PREVIOUS COMMENTS:


def integrate_user_feedback(questions, feedback_list):
    # Integrate user feedback to continuously improve question quality
    all_feedback=[]

    for feedback in feedback_list:
        question_id = feedback.get("question_id")
        comment = feedback.get("comment")
        all_feedback.append(comment)


        # Find the question with the corresponding question_id in the questions list
        for question in questions:
            if question.get("question_id") == question_id:
                # Update the question with user feedback
                question["user_comment"] = comment


    #def summarize_prompt(all_feedback, api_key="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", model="gpt-3.5-turbo-instruct", max_chunk=2048):
    api_key="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"
    model="gpt-3.5-turbo-instruct"
    max_chunk=2048
    openai.api_key = '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'

    try:
        
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt="I will provide you with a feedback from an exam, you must summarize the feedback so that next time the questions will be relevant and in and accurate manner,the feedback is: "+ " ".join(all_feedback),
            max_tokens=1400,
            n=1,
            stop=None,
            temperature=0.8,
            )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        print("Error with OpenAI API: ", str(e))
    
    

    

