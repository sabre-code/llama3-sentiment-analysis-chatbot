import streamlit as st

import psycopg2

#print("connecting to postgresql...")
connection = psycopg2.connect(host='localhost',database='sentiment',user='postgres',password='admin')

cursor = connection.cursor()



def plot_sentiment_distribution():
    cursor.execute("SELECT sentiment, count FROM sentiment_count")
    results = cursor.fetchall()
    sentiment_counts = {}

    for row in results:
        sentiment, count = row
        sentiment_counts[sentiment] = count
    st.title("Sentiment Distribution")
    st.bar_chart(sentiment_counts)



plot_sentiment_distribution()