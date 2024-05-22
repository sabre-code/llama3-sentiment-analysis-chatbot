import streamlit as st
import time
import requests
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import psycopg2

#print("connecting to postgresql...")
connection = psycopg2.connect(host='localhost',database='sentiment',user='postgres',password='admin')

cursor = connection.cursor()

analyzer = SentimentIntensityAnalyzer()


HF_KEY = st.secrets["HF_KEY"]

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": f"Bearer {HF_KEY}"}

st.title("Llama 3 Chatbot 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def response_generator(prompt):
    prompt = {
        "inputs": prompt
    }
    response = requests.post(API_URL, headers=headers, json=prompt)
    data = json.loads(response.content)
    text = data[0]["generated_text"]
    return text


def sentiment_analysis(text):
    sentiment = analyzer.polarity_scores(text)
    compound_score = sentiment["compound"]

    if compound_score > 0.05:
        cursor.execute("UPDATE sentiment_count SET count = count + 1 WHERE sentiment = 'positive';")
    elif compound_score < -0.05:
        cursor.execute("UPDATE sentiment_count SET count = count + 1 WHERE sentiment = 'negative';")
    else:
        cursor.execute("UPDATE sentiment_count SET count = count + 1 WHERE sentiment = 'neutral';")

    connection.commit()


    
    
    

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role":"user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        response = response_generator(prompt)
        st.write(response)
        sentiment_analysis(prompt)
       

    st.session_state.messages.append({"role":"assistant", "content": response})
