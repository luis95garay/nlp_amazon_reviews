from typing import Dict
import json
import streamlit as st
import requests


def predict_req(new_data: Dict):
    url = "http://sentiment_classification:8000/pytorch_predict"

    payload = json.dumps(new_data)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    details = json.loads(response.text)
    return details['data']


st.set_page_config(layout="centered")

st.title("Sentiment Analysis :no_mouth: :watermelon:")
review = st.text_input("Review", 'It is the worst product I have ever bought')

submitted = st.button("Submit")
if submitted:
    new_data = {
        "text": review
    }
    result = predict_req(new_data)
    if result['class_name'] == 'Positive':
        st.title((f"The prediction is: {result['class_name']} :smile: with a score of {result['score']:.2f}"))
    else:
        st.title((f"The prediction is: {result['class_name']} :sweat: with a score of {result['score']:.2f}"))
