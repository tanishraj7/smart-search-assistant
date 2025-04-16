import streamlit as st #type: ignore
import time
from PyPDF2 import PdfReader #type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter #type: ignore
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings #type: ignore
import google.generativeai as genai #type: ignore
from langchain.vectorstores import FAISS #type: ignore
from langchain_google_genai import ChatGoogleGenerativeAI #type: ignore
from langchain.chains.question_answering import load_qa_chain #type: ignore
from langchain.prompts import PromptTemplate #type: ignore
import streamlit.components.v1 as components #type:ignore
from dotenv import load_dotenv #type: ignore
from langchain.globals import set_llm_cache #type: ignore
from langchain.cache import InMemoryCache #type:ignore

load_dotenv()
os.getenv("GOOGLE_API_KEY")

genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <div class="jumbotron jumbotron-fluid">
        <div class="container">
            <h1 class="display-4">PdfBud</h1>
            <p class="lead">Talk to your docs.</p>
        </div>
    </div>
    """,
    height=250,
)

set_llm_cache(InMemoryCache())

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            extracted_text= page.extract_text()
            if extracted_text:
                text += extracted_text
    return text

def get_text_chunks(text):
    text_splitter= RecursiveCharacterTextSplitter(chunk_size= 10000, chunk_overlap= 1000)
    chunks= text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings= GoogleGenerativeAIEmbeddings(model= "models/embedding-001")
    vector_store= FAISS.from_texts(text_chunks, embedding= embeddings)
    vector_store.save_local("faiss_index")
    
    
def get_conversational_chain():
    prompt_template= """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in provided context but if the question is relevant to the input_documents only then find shortest possible answer from your knowledge and say "answer not available in context but here is what I know", and answer in one line, but do not provide wrong answers and remember Tanish Raj Singh and Yashica Goel made you\n\n
    Context:\n {context}?\n
    Question:\n {question}\n
    
    Answer:
    """
    
    model= ChatGoogleGenerativeAI(model= "gemini-1.5-pro", temperature= 0.4)
    prompt= PromptTemplate(template= prompt_template, input_variables= ['context', 'question'])
    chain= load_qa_chain(model, chain_type= "stuff", prompt= prompt)
    
    return chain
    
    
def user_input(user_question):
    embeddings= GoogleGenerativeAIEmbeddings(model= "models/embedding-001")
    new_db= FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization= True)
    # docs= new_db.similarity_search(user_question)
    # chain= get_conversational_chain()
    docs_with_scores= new_db.similarity_search_with_score(user_question, k=4)
    threshold= 0.5
    
    filtered_docs= [doc for doc, score in docs_with_scores if score > threshold]
    
    start= time.time()
    # response= chain({
    #     "input_documents":docs, "question": user_question
    # }, return_only_outputs= True)
    if filtered_docs:
        chain= get_conversational_chain()
        response= chain({
            "input_documents": filtered_docs,
            "question": user_question
        }, return_only_outputs= True)
    else:
        response= {"answer": "Answer not available in context."}
    
    end= time.time()
    total_time= end - start-1
    
    print(response)
    st.write("🤖: ", response["output_text"])
    st.write(f"🕒 Answer Retrieval Time: {total_time:.4f} seconds")
    
def main():
    
    st.markdown("💬 **Chat with your PDF files effortlessly!** Upload a PDF, ask questions, and get instant answers.")

    st.divider()  # Adds a visual separator

    # PDF Upload Section
    st.subheader("📂 Upload Your PDF")
    pdf_docs = st.file_uploader("Select one or more PDF files", accept_multiple_files=True, type=["pdf"])

    if st.button("📥 Process PDFs"):
        if pdf_docs:
            with st.spinner("🔄 Extracting text from PDFs..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
            st.success("✅ PDF processed successfully! Now, ask a question below. 💡")
        else:
            st.warning("⚠️ Please upload at least one PDF before submitting.")

    st.divider()

    # User Question Input Section
    st.subheader("💡 Ask a Question")
    user_question = st.text_input("🔎 Type your question and press Enter:")

    if user_question:
        user_input(user_question)

    st.divider()

    # Expandable Help Section
    with st.expander("ℹ️ How It Works"):
        st.write("""
        1️⃣ **Upload PDFs** using the file uploader above.  
        2️⃣ Click **Process PDFs** to extract and store text.  
        3️⃣ Type a **question** in the input box and press Enter.  
        4️⃣ The chatbot retrieves relevant answers from the document.  
        """)

    st.caption("🤖 Powered by AI | Created with ❤️ using Streamlit")
    
    
if __name__ == "__main__":
    main()
    
    



    