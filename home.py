import streamlit as st #type:ignore
import streamlit.components.v1 as components #type:ignore
import pandas as pd #type:ignore

st.set_page_config(page_title="EduBud Smart Search", page_icon="🚀", layout="centered")

components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div class="jumbotron jumbotron-fluid">
        <div class="container">
            <h1 class="display-4">Edu-Bud</h1>
            <p class="lead">Smart Search AI assistant: Data Enrichment Tool</p>
        </div>
    </div>
    """,
    height=300,
)


# --- Header Section ---
st.markdown(
    """
    <style>
        .title {
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .section-header {
            font-size: 28px;
            color: #4B8BBE;
            margin-top: 30px;
        }
        .team-name {
            font-weight: bold;
            font-size: 20px;
            color: #1f77b4;
        }
        .info {
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Project Description ---
st.markdown("### 🔍 About the Project")
st.write("""
Our **Smart Question-Answering AI** efficiently processes both text-based and PDF-based queries, ensuring accurate and context-aware responses.
Powered by **FAISS** for similarity search and **embeddings** for conceptual understanding, the system enhances retrieval efficiency and precision.
Compared to a non-FAISS model, it demonstrates significant performance improvements.
The AI intelligently filters out-of-context queries, maintaining relevance and accuracy.
With a **user-friendly Streamlit interface**, users can seamlessly interact, upload documents, and get precise answers in real time. 🚀
""")

# --- Models Section ---
st.markdown("### 🧠 Our Models")

col1, col2 = st.columns(2)

with col1:
    st.subheader("TextBud")
    st.write("""
    Our model first takes the context as input, tokenizes it, and feeds it into a **transformer-based encoder**.
    It then identifies the start and end indices of the most probable answer span,
    scores all possible answers, and extracts the highest scoring one.
    """)

with col2:
    st.subheader("PdfBud")
    st.write("""
    Our AI extracts text from PDFs, splits it into chunks, and embeds them using **Google Generative AI embeddings (0/1)**.
    These are stored in a **FAISS index** for efficient retrieval. Upon a user's query, the system searches for the most relevant chunk
    and responds using **Gemini Pro (Temperature=0.4)** for accurate, context-aware answers.
    """)
    
#---Plot---
st.subheader('Increasing usage of AI in data and education ⤵️')

data = [
    [10],
    [20],
    [40],
    [65],
    [80],
    [85]
]


chart_data= pd.DataFrame(
    data,
    columns=['Rate']
)

st.bar_chart(chart_data)

# --- Team Section ---
st.markdown("### 👥 About Us")

team_col1, team_col2 = st.columns(2)

with team_col1:
    st.markdown('<div class="team-name">Tanish Raj Singh</div>', unsafe_allow_html=True)
    st.write("""
    BTECH CSE '26 batch student from Manipal University Jaipur and a **Student Placement Coordinator**.
    Contributed efficiently in **development and deployment** of Edu-Bud 🤖
    """)
    btn1, btn2 = st.columns(2)
    btn1.link_button('GitHub', url='https://github.com/tanishraj7')
    btn2.link_button('LinkedIn', url='https://www.linkedin.com/in/tanishrajsingh/')

with team_col2:
    st.markdown('<div class="team-name">Yashica Goel</div>', unsafe_allow_html=True)
    st.write("""
    BTECH CSE '26 batch student from Manipal University Jaipur.
    Contributed efficiently in **research and documentation** of Edu-Bud 🤖
    """)
    btn3, btn4 = st.columns(2)
    btn3.link_button('GitHub', url='https://github.com/yashica1704')
    btn4.link_button('LinkedIn', url='https://www.linkedin.com/in/yashica-goel/')

