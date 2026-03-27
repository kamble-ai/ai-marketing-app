from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class RequestData(BaseModel):
    product: str
    audience: str
    platform: str


@app.get("/")
def home():
    return {"message": "AI Marketing SaaS Running 🚀"}


@app.post("/generate")
def generate(data: RequestData):
    try:
        prompt = f"""
You are an AI Marketing Expert.

Create a COMPLETE marketing plan.

Product: {data.product}
Target Audience: {data.audience}
Platform: {data.platform}

Give output in clean structured format:

1. 🎯 Strategy
2. 🧠 Psychological Hook Idea
3. ✍️ 5 Viral Captions (very engaging & curiosity-based)
4. 🔥 Top 5 Trending Hashtags
5. 📢 Campaign Plan (step-by-step)
6. ⚠️ Do's and Don'ts
7. 💬 Pin Comment (to increase engagement)
8. ⚖️ Disclaimer (if needed)
9. 🚀 Motivation Tips for consistency
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "campaign": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}