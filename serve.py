import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load .env for GROQ_API_KEY
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the model
model = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)

# Set up prompt and parser
system_template = "translate the following into {language} :"
prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])
output_parser = StrOutputParser()
chain = prompt | model | output_parser

# Streamlit UI
st.set_page_config(page_title="Groq Translator", layout="centered")
st.title("🌍 Language Translator using LangChain + Groq")

text = st.text_area("Enter text to translate:", height=150)
language = st.selectbox("Choose target language:", ["Hindi", "Spanish", "French", "German", "Japanese"])

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Translating..."):
            try:
                result = chain.invoke({"language": language, "text": text})
                st.success("Translation:")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")

