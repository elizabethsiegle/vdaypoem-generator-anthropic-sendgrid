from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import dotenv_values
from exa_py import Exa
import os
from PIL import Image
import requests
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
     Mail, Attachment, FileContent, FileName, FileType, Disposition)
import streamlit as st

with open('./style/style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

config = dotenv_values(".env")
EXA_API_KEY = config.get('EXA_API_KEY')
SENDGRID_API_KEY = config.get('SENDGRID_API_KEY')
ANTHROPIC_API_KEY = config.get('ANTHROPIC_API_KEY')

def main():
    st.title("Love Letter Generator❤️ 💌") 
    st.write("Built w/ Anthropic, SendGrid, Streamlit, Exa, and Replit") 
    image = Image.open('pikalove.png')
    st.image(image)
    
    receiver_name = st.text_input("Letter receiver name")
    receiver_description = st.text_area("""
    Describe the person who you'd like to receive the love letter❤️💌""",
    """
    What do they like? What do you like about them? What's a funny memory with them?
    """)

    options = st.multiselect(
        'What would you like your love letter to include',
        ['limerick', 'haiku', 'humor', 'Star Wars⭐️🔫 quotes', 'Shrek reference', 'Taylor Swift lyrics🎶', 'Klay Thompson quote🏀'],
        ['Star Wars⭐️🔫 quotes', 'limerick', 'Shrek reference'])

    st.write('You selected:', options)

    user_email = st.text_input("Email to send love letter to📧", "lol@gmail.com (you deserve one too!)")

    if st.button('Generate love letter w/ AI 🧠🤖'):
        # exa semantic search,
        with st.spinner('Processing📈...'):
            PROMPT= f"Craft a love letter to the external data: {competitors}"
            anthropic = Anthropic(
                api_key=ANTHROPIC_API_KEY
            )
            
            completion = anthropic.completions.create(
                model="claude-2.1",
                max_tokens_to_sample=700,
                prompt=f"{HUMAN_PROMPT}: {PROMPT}. {AI_PROMPT}",
            )
            print(completion.completion)



    footer="""
    <footer>
        <p>Developed with ❤ in SF🌁</p> 
        <p>✅ out the code on <a href="https://github.com/elizabethsiegle/loveletter-generator-anthropic-sendgrid" target="_blank">GitHub</a></p>
    </footer>
    """
    st.markdown(footer,unsafe_allow_html=True)

if __name__ == "__main__":
    main()