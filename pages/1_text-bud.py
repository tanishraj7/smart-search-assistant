import streamlit as st #type:ignore
import streamlit.components.v1 as components #type:ignore
from transformers import pipeline

components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div class="jumbotron jumbotron-fluid">
        <div class="container">
            <h1 class="display-4">TextBud</h1>
            <p class="lead">Talk to your article.</p>
        </div>
    </div>
    """,
    height=250,
)

@st.cache_resource

def load_model():
    model= pipeline("question-answering")
    return model

agent= load_model()

st.title("Q&A text based model")
article= st.text_area("paste your article here...")
ques= st.text_input("What is your question?")
bttn= st.button("Get Answer")

with st.spinner("Getting your answers..."):
    if ques and article and bttn:
        answer= agent(question= ques, context= article)
        st.success(answer['answer'])
        
with st.expander("ℹ️ How It Works"):
        st.write("""
        1️⃣ Paste your article.  
        2️⃣ Ask your question.  
        3️⃣ click on the get answer button.  
        4️⃣ The chatbot retrieves relevant answers from your article.  
        """)

st.caption("🤖 Powered by AI | Created with ❤️ using Streamlit")
