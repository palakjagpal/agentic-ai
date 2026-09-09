from fastapi import FastAPI
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