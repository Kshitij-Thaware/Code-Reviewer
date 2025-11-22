import streamlit as st
from openai import OpenAI


def get_code_review(code):
    prompt = f"Please review the following code and provide suggestions for improvement:{code}"
    
    try:
        
        client = OpenAI(api_key=st.secrets['OPENAI_API']['OPENAI_API'])

        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system", #context
            "content": [
                {
                "type": "text",
                "text": "You are an expert programmer specialized in reviewing code for optimization of time and computation complexity."
                }
            ]
            },
            {
            "role": "user", #query
            "content": [
                {
                "type": "text",
                "text": prompt
                }
            ]
            },            
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
        )
        
        review = response.choices[0].message.content
        return review
    
    except Exception as e:
        return f"An error occurred: {e}"