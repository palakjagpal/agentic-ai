from fastapi import FastAPI,Query
from google import genai
import os
from dotenv import load_dotenv
from httpx import Client

app=FastAPI()

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL="gemini-3.5-flash-lite"

@app.get("/home")
def gethome():
    return{
        "message":"Welcome to Gemini FastAPI"
    }

@app.get("/ask")
def ask(question : str = Query(...,description="Enter your question here")):
    response=client.models.generate_content(
        model=MODEL,
        contents=question
    )
    return{
        "question":question,
        "answer":response.text
    }