import streamlit as st
import pdfplumber
import time
import requests

# Function to extract questions from the NAQT PDF
def extract_questions_from_pdf(url):
    response = requests.get(url)
    with open("quiz_set.pdf", "wb") as f:
        f.write(response.content)

    with pdfplumber.open("quiz_set.pdf") as pdf:
        questions = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Process each page's text to extract questions and answers
                sections = text.split("\n")
                for section in sections:
                    if section.strip().startswith("Q"):
                        question = section.strip()  # Assuming question starts with 'Q'
                        questions.append(question)
        return questions

# Slow typing effect for the question display
def slow_typing(question, delay=0.1):
    for char in question:
        st.write(char, end='', flush=True)
        time.sleep(delay)

# Main Streamlit App
st.title("Quizbowl Game")
st.write("Enter the URL of an NAQT question set (PDF format)")

# User Input: URL for the NAQT PDF
pdf_url = st.text_input("Enter NAQT Set URL:", "https://www.naqt.com/samples/middle-school-series.pdf")

if pdf_url:
    try:
        # Extract questions from the provided URL
        questions = extract_questions_from_pdf(pdf_url)

        # Display the first question
        if questions:
            question_idx = 0
            score = 0

            while question_idx < len(questions):
                st.subheader(f"Question {question_idx + 1}:")
                slow_typing(questions[question_idx])  # Slowly type out the question
                
                # Allow the user to input their answer with a unique key
                user_answer = st.text_input("Your Answer:", key=f"answer_{question_idx}")
                
                if user_answer:  # When the user provides an answer
                    # Check answer (for simplicity, this is just a placeholder check)
                    # In a real scenario, you'd check the answer against the correct one.
                    # For now, we'll just assume every answer is correct.
                    score += 1
                    
                    # Move to the next question after a delay
                    st.write(f"Correct! Your score: {score}")
                    time.sleep(2)
                    question_idx += 1

                # Adding an option to exit or restart the quiz
                if question_idx >= len(questions):
                    st.subheader("Quiz Over!")
                    st.write(f"Final score: {score}")
                    if st.button("Restart Quiz"):
                        question_idx = 0
                        score = 0
    except Exception as e:
        st.error(f"Error loading the PDF: {e}")
