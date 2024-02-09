from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import dotenv_values
from exa_py import Exa
import os
from PIL import Image
import replicate
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
anthropic = Anthropic(
    api_key=ANTHROPIC_API_KEY
)

def main():
    st.title("Love Poem Generator❤️ 💌") 
    st.write("Built w/ Anthropic, SendGrid, Streamlit, Exa, Replicate, and Replit") 
    image = Image.open('pikalove.png')
    st.image(image)
    
    receiver_name = st.text_input("Poem receiver name")
    receiver_description = st.text_area("""
    Describe the person who you'd like to receive the poem""",
    """
    What do they like? What do you like about them? What's a funny memory with them?
    """)
    model_toggle = st.radio("What LLM would you like to use", # lol it rhymes
            [":rainbow[llama-2-70b-chat]", "***Claude***"],
            captions = ["Hosted on Replicate", "Thank you, Anthropic"]) 

    addons = st.multiselect(
        'What would you like your love letter to include',
        ['humor', 'Star Wars quotes', 'Shrek reference', 'Taylor Swift lyrics', 'Klay Thompson quote'],
        ['Star Wars quotes', 'Shrek reference'])

    st.write('You selected:', addons)

    user_email = st.text_input("Email to send love poem to📧", "lol@gmail.com (you deserve one too!)")
    poem = ''

    if st.button('Generate a poem w/ AI 🧠🤖'):
        with st.spinner('Processing📈...'):
            PROMPT1 = f"""
                You are a copy editor. Edit the following blurb and return only that edited blurb, ensuring the only pronouns used are "I": {receiver_description}. 
                Next, parse out the items from the following string so it's only a list of items and no brackets or quotes: {addons}
                Add onto the edited blurb the list of items and nothing else. There should be no preamble.
            """
            if model_toggle == "***Claude***":
                completion1 = anthropic.completions.create(
                    model="claude-instant-1.2", # claude-2.1
                    max_tokens_to_sample=700,
                    prompt=f"{HUMAN_PROMPT}: {PROMPT1}. {AI_PROMPT}",
                )
                print(completion1.completion)
                newPronouns = completion1.completion

                PROMPT= f"""
                Please make me laugh by writing a short, silly, lighthearted, complimentary, lovey-dovey poem about the following person named {receiver_name}. 
                <receiver_description>{newPronouns}</receiver_description>. 
                I would enjoy it if the poem also jokingly included some of the following: {addons}. 
                Return only the poem and nothing else.
                """
                print(PROMPT)
                
                completion = anthropic.completions.create(
                    model="claude-2.1",
                    max_tokens_to_sample=1000,
                    prompt=f"{HUMAN_PROMPT}: {PROMPT}. {AI_PROMPT}",
                )
                poem = completion.completion
                print(poem)
                st.write(f'Generated poem:  {poem}')

            elif model_toggle == ":rainbow[llama-2-70b-chat]":
                editpronouns = replicate.run(
                    "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                    input={
                        "prompt": PROMPT1,
                        "max_new_tokens": 700
                    }
                )
                newpronounsblurb = ''
                for item in editpronouns:
                    newpronounsblurb+=item
                    print(item, end="")
                print("newpronounsblurb ", newpronounsblurb)

                PROMPT2= f"""
                Please make me laugh by writing a short, silly, lighthearted, complimentary, lovey-dovey poem about the following person named {receiver_name}. 
                <receiver_description>{newpronounsblurb}</receiver_description>. 
                I would enjoy it if the poem also jokingly included some of the following: {addons}. 
                Return only the poem and nothing else.
                """
                print(PROMPT2)

                poem = replicate.run(
                    "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                    input={
                        "prompt": PROMPT2,
                        "max_new_tokens": 1000
                    }
                )
                newpoem = ''
                for item in poem:
                    newpoem+=item
                    print(item, end="")
                print("newpoem ", newpoem)
                st.write(f'The generated poem: {newpoem}')


            message = Mail(
                from_email='love@poem.com',
                to_emails=user_email,
                subject='A personal poem for you!❤️',
                html_content=f'{poem}'
            )

            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code, response.body, response.headers)
            if response.status_code == 202:
                st.success("Email sent! Tell your ✨friend✨ to check their email for their poem")
                print(f"Response Code: {response.status_code} \n Email sent!")
            else:
                st.warning("Email not sent--check console")


    footer="""
    <footer>
        <p>Developed with ❤ in SF🌁</p> 
        <p>✅ out the code on <a href="https://github.com/elizabethsiegle/loveletter-generator-anthropic-sendgrid" target="_blank">GitHub</a></p>
    </footer>
    """
    st.markdown(footer,unsafe_allow_html=True)

if __name__ == "__main__":
    main()