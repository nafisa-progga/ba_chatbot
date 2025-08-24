from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA

# Initialize the models. No need to configure the API key here,
# as it's done once in main.py.
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", temperature=0.2)

# --- Dummy Data and Vector Store Creation ---
def create_dummy_db():
    """
    Creates and returns a dummy FAISS vector store.

    This function demonstrates how to build a vector database using sample documents.
    It simulates a real-world scenario where you would load your own FAQ data.
    """
    print("Creating dummy FAISS vector store for demonstration...")

    # Sample documents with common questions and answers
    documents = [
        Document(page_content="What is the process for a business analysis? The process starts with a needs assessment, then moves to requirements gathering, solution design, and finally, implementation and validation."),
        Document(page_content="How do you handle scope creep? We manage scope creep through a formal change control process, where any new requests are evaluated for their impact on budget, timeline, and resources before being approved."),
        Document(page_content="What are the key responsibilities of a business analyst? A business analyst's key responsibilities include defining requirements, facilitating communication between stakeholders, documenting business processes, and ensuring the final solution meets the business needs."),
        Document(page_content="Can you explain the difference between a business requirement and a functional requirement? A business requirement is a high-level statement of a business goal, while a functional requirement describes what the system must do to meet that goal."),
        Document(page_content="What is a stakeholder? A stakeholder is any person, group, or organization who can affect or be affected by a project. This includes clients, team members, managers, and end-users."),
    ]

    # Create the vector store from the dummy documents
    db = FAISS.from_documents(documents, embeddings)

    print("Dummy FAISS vector store created successfully.")
    return db

# --- Retrieval-Augmented Generation (RAG) Chain ---
def get_rag_response(query: str):
    """
    Retrieves information from the vector store and generates a response.
    """
    db = create_dummy_db()
    
    # Create a retriever from the vector store
    retriever = db.as_retriever(search_kwargs={"k": 2})

    # Set up the prompt template
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a helpful business analyst assistant. Use the following context to answer the question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context:
        {context}

        Question:
        {question}

        Helpful Answer:
        """
    )
    
    # Create the RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )
    
    # Get the response
    result = qa_chain({"query": query})
    return result["result"]
