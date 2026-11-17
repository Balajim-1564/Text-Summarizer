from datetime import datetime
from io import BytesIO
import os

import streamlit as st
from pypdf import PdfReader
from pypdf.errors import PdfReadError

#from summarizer import generate_summary
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

from summarizer import summarize_text

st.title("Text Summarizer")

if "summary_history" not in st.session_state:
    st.session_state.summary_history = []

input_source = st.radio("Choose input method:", ["Paste Text", "Upload a file"])

source_text = ""
if input_source == "Paste Text":
    source_text = st.text_area("Enter the text you want to summarize:")
elif input_source == "Upload a file":
    uploaded_file = st.file_uploader("Upload a text or PDF file", type = ["txt", "pdf"])
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            source_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            try:
                pdf_reader = PdfReader(uploaded_file)
                source_text = ""
                for page in pdf_reader.pages:
                    source_text += page.extract_text()
            except PdfReadError:
                st.error("Error reading PDF file. Please ensure the file is not corrupted.")


# purpose = st.text_area("Enter the text you want to summarize:")
summary_length = st.selectbox("Select the summary Length:", ["Short", "Medium", "Detailed"])
summary_format = st.selectbox("Select the summary format:", ["Paragraph", "Bullet_Points", "Key Takeaways"])


if st.button("Generate Summary"):
    if source_text:
        summary = summarize_text(source_text, summary_length.lower(), summary_format.lower())
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Please enter some text to summarize.")

                       