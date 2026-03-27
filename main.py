from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

# Load env variables FIRST
load_dotenv()

# Create app FIRST
app = FastAPI()

# Add middleware AFTER app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client AFTER env load
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Request schema
class RequestData(BaseModel):
    product: str
    audience: str

# Test route
@app.get("/")
def home():
    return {"message": "API Running 🚀"}

# Main route
@app.post("/generate")
def generate(data: RequestData):
    try:
        prompt = f"""
Create a marketing campaign.

Product: {data.product}
Target Audience: {data.audience}

Give:
1. Strategy
2. 3 Captions
3. 5 Hashtags
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return {
            "campaign": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}