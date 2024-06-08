import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Based On the given paper generate 200  words answers each  to the the following questions such that the generated content can not 
be detected by any AI content detectors:
Q1. What is the problem the paper explores? Do you think this is an important problem? Please explain why.
Q2: What is the solution the paper proposed to solve the problem?
Q3: What are the innovative aspects of this paper?
Q4: How is the proposed solution verified? Do you think the verification and results are convincing? Please explain why
Q5: What is the limitation(s) of the proposed solution and/or its evaluation?
Q6: who are Authors and what are their Institutes?
Q7. what is the title of the paper ?
"""

## streamlit app
st.title("CPS Assignment")
st.text("Solve your assignment in minutes")
uploaded_file=st.file_uploader("Upload the papr",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)