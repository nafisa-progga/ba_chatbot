# app/routers/agent.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from app.services.rag_service import get_rag_response
from app.services.nl_to_sql_service import get_sql_query
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

agent_router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

# Use a lightweight model specifically for intent classification
llm_classifier = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", temperature=0.1)

# Define a prompt template for intent classification
INTENT_PROMPT_TEMPLATE = """
You are a smart AI classifier. Your task is to analyze a user's question and determine its intent.
Based on the question, classify the intent into one of two categories:

1.  DATABASE_QUERY: The question is asking for information that can be found in a database.
    This includes questions about employees, departments, products, or any structured data.
    Examples: "How many employees?", "List all products", "Who works in HR?", "What is the average salary?".

2.  GENERAL_QUERY: The question is general and requires a non-database answer.
    Examples: "What is a stakeholder?", "Tell me about business analysis", "How do I handle scope creep?".

Respond with ONLY the classification name, without any other text or punctuation.
Example: "DATABASE_QUERY"

User's question: {question}

Classification:
"""

def classify_query_intent(query: str) -> str:
    """
    Classifies the user's query as either DATABASE_QUERY or GENERAL_QUERY.
    """
    prompt = PromptTemplate(
        input_variables=["question"],
        template=INTENT_PROMPT_TEMPLATE
    )
    chain = LLMChain(llm=llm_classifier, prompt=prompt)
    
    # Run the classification chain
    intent = chain.run(question=query).strip().upper()
    
    # Simple check to ensure a valid classification is returned
    if "DATABASE_QUERY" in intent:
        return "DATABASE_QUERY"
    return "GENERAL_QUERY"


@agent_router.post("/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest) -> Dict[str, Any]:
    """
    Handles chat requests by routing them to the appropriate service based on intent.
    """
    query = request.query
    
    # Classify the query intent using the new function
    intent = classify_query_intent(query)
    
    print(f"Query: '{query}' classified as: {intent}")
    
    if intent == "DATABASE_QUERY":
        response = get_sql_query(query)
    else:
        response = get_rag_response(query)
    
    return {"answer": response}
