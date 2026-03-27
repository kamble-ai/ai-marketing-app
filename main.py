from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_generate(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
@app.get("/")
def home():
    return FileResponse("index.html")

# =========================
# INSTAGRAM AGENT
# =========================
def instagram_agent(product, audience):
    prompt = f"""
Create a HIGH-CONVERTING Instagram marketing plan.

Product: {product}
Target Audience: {audience}

Give output in this format:
1. Strategy
2. Growth Plan
3. Do's and Don'ts
4. Top 5 Psychological Captions
5. Top 5 Viral Hashtags
6. Disclaimer
7. Pin Comment
"""
    return ai_generate(prompt)

# =========================
# FACEBOOK AGENT
# =========================
def facebook_agent(product, audience):
    prompt = f"""
Create a HIGH-CONVERTING Facebook Ads strategy.

Product: {product}
Target Audience: {audience}

Include:
- Strategy
- Growth Plan
- Do's and Don'ts
- 5 Captions
- Hashtags
- CTA
"""
    return ai_generate(prompt)

# =========================
# GOOGLE ADS AGENT
# =========================
def google_agent(product, audience):
    prompt = f"""
Create a HIGH-CONVERTING Google Ads campaign.

Product: {product}
Target Audience: {audience}

Include:
- Strategy
- Keywords
- Headlines
- Do's and Don'ts
- CTA
"""
    return ai_generate(prompt)

# =========================
# YOUTUBE SHORTS AGENT
# =========================
def youtube_short_agent(product, audience):
    prompt = f"""
Create a viral YouTube Shorts strategy.

Product: {product}
Target Audience: {audience}

Include:
- Hook
- Strategy
- Captions
- Hashtags
"""
    return ai_generate(prompt)

# =========================
# YOUTUBE LONG AGENT
# =========================
def youtube_long_agent(product, audience):
    prompt = f"""
Create a YouTube long video strategy.

Product: {product}
Target Audience: {audience}

Include:
- Content plan
- Titles
- SEO strategy
- Growth tips
"""
    return ai_generate(prompt)

# =========================
# MAIN ROUTE
# =========================
@app.post("/generate")
async def generate(data: dict):
    product = data.get("product")
    audience = data.get("audience")
    platform = data.get("platform")

    if not product or not audience or not platform:
        return {"error": "Missing input"}

    platform = platform.lower()

    if platform == "instagram":
        result = instagram_agent(product, audience)

    elif platform == "facebook ads":
        result = facebook_agent(product, audience)

    elif platform == "google ads":
        result = google_agent(product, audience)

    elif platform == "youtube shorts":
        result = youtube_short_agent(product, audience)

    elif platform == "youtube long":
        result = youtube_long_agent(product, audience)

    elif platform == "all":
        result = "\n\n".join([
            instagram_agent(product, audience),
            facebook_agent(product, audience),
            google_agent(product, audience),
            youtube_short_agent(product, audience),
            youtube_long_agent(product, audience),
        ])

    else:
        return {"error": "Invalid platform"}

    return {"campaign": result}