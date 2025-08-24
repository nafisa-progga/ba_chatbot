from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment. This will fail if not set.
# The 'get' method is used to avoid a KeyError if the variable is missing.
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please add it to your .env file.")

# Configure the Google Generative AI library once for the entire application
genai.configure(api_key=api_key)

# Initialize the FastAPI app
app = FastAPI(title="BA Chatbot")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include the agent router after the API key has been configured
from app.routers.agent import agent_router
app.include_router(agent_router, prefix="/api")

@app.get("/")
def read_root():
    """
    Root endpoint for a simple health check.
    """
    return {"message": "Welcome to the BA Chatbot API!"}
