from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

# Load env
load_dotenv()

app = FastAPI()

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Request schema
class RequestData(BaseModel):
    product: str
    audience: str
    platform: str

@app.get("/")
def home():
    return {"message": "AI SaaS Multi-Agent Running 🚀"}

# 🔥 MULTI-AGENT SYSTEM
@app.post("/generate")
def generate(data: RequestData):
    try:

        # 🧠 Agent 1: Strategy
        strategy_prompt = f"""
        Create a marketing STRATEGY.

        Product: {data.product}
        Audience: {data.audience}
        Platform: {data.platform}

        Give:
        - Clear campaign idea
        - Content direction
        """

        strategy = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": strategy_prompt}]
        ).choices[0].message.content

        # ✍️ Agent 2: Content (Captions)
        content_prompt = f"""
        Generate HIGH CONVERTING psychological captions.

        Platform: {data.platform}
        Product: {data.product}

        Give 5 captions:
        - curiosity driven
        - emotional trigger
        - short and viral
        """

        captions = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": content_prompt}]
        ).choices[0].message.content

        # 🔍 Agent 3: SEO
        seo_prompt = f"""
        Generate SEO hashtags.

        Product: {data.product}
        Platform: {data.platform}

        Give:
        - Top 10 hashtags
        - Trending keywords
        """

        hashtags = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": seo_prompt}]
        ).choices[0].message.content

        # 📈 Agent 4: Growth + Do/Don't
        growth_prompt = f"""
        Give growth strategy.

        Product: {data.product}
        Platform: {data.platform}

        Include:
        - Do’s
        - Don’ts
        - Motivation tips
        """

        growth = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": growth_prompt}]
        ).choices[0].message.content

        # 📦 Combine all agents
        final_output = f"""
🔥 AI MARKETING PLAN

================ STRATEGY ================
{strategy}

================ CAPTIONS ================
{captions}

================ SEO & HASHTAGS ================
{hashtags}

================ GROWTH GUIDE ================
{growth}
"""

        return {"campaign": final_output}

    except Exception as e:
        return {"error": str(e)}