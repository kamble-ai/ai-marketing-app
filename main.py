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

# CORS (allow frontend)
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


# ===============================
# MULTI-AGENT GENERATOR
# ===============================
@app.post("/generate")
async def generate(data: dict):
    product = data.get("product")
    audience = data.get("audience")
    platform = data.get("platform")

    if not product or not audience or not platform:
        return {"error": "Missing input"}

    platform = platform.lower()


    # ===============================
    # INSTAGRAM AGENT
    # ===============================
    def instagram_agent(product, audience):
    prompt = f"""
    Create a HIGH-CONVERTING Instagram marketing plan.

    Product: {product}
    Target Audience: {audience}

    Give output in this format:

    1. Strategy (clear steps)
    2. Growth Plan
    3. Do's and Don'ts
    4. Top 5 Psychological Captions
    5. Top 5 Viral Hashtags (latest trends)
    6. Disclaimer
    7. Pin Comment (high converting CTA)
    """

    return ai_generate(prompt)


🎯 Strategy:
- Use reels (3-5/week)
- Hook in first 3 seconds
- Focus on transformation content

📈 Growth Plan:
- Collaborate with influencers
- Use trending audio
- Post at peak hours (6-9 PM)

✅ Do’s:
- Use subtitles
- Strong hooks
- High-quality visuals

❌ Don’ts:
- Don’t post random content
- Don’t ignore engagement
- Don’t use low-quality videos

🧠 Top 5 Psychological Captions:
1. 99% ignore this… don’t be one
2. Your future depends on today
3. No excuses. Start now
4. Discipline beats motivation
5. Change starts today

🔥 Hashtags:
#fitness #gym #reels #viral #india

⚠️ Disclaimer:
Results may vary based on effort

📌 Pin Comment:
DM NOW for exclusive offer
"""


    # ===============================
    # FACEBOOK AGENT
    # ===============================
    def facebook_agent():
        return f"""
📘 FACEBOOK ADS

🎯 Strategy:
- Target specific audience (18–25)
- Use video + testimonials
- Strong CTA (Join Now)

📈 Growth Plan:
- Retarget users
- A/B testing
- Use conversion campaigns

✅ Do’s:
- Clear offer
- Strong headline
- Use proof/testimonials

❌ Don’ts:
- Don’t use broad targeting
- Don’t ignore analytics
- Don’t use weak creatives

🧠 Top 5 Psychological Captions:
1. Start your journey today
2. Limited student offer
3. Transform now
4. Join thousands already growing
5. Best decision you’ll make

🔥 Hashtags:
#facebookads #marketing #fitness #ads #growth

⚠️ Disclaimer:
Offer valid for limited time

📌 Pin Comment:
Click Sign Up now!
"""


    # ===============================
    # GOOGLE ADS AGENT
    # ===============================
    def google_agent():
        return f"""
🔍 GOOGLE ADS

🎯 Strategy:
- Target high-intent keywords
- Focus on “near me” searches

📈 Growth Plan:
- Optimize CTR
- Improve landing page
- Use extensions

✅ Do’s:
- Use strong keywords
- Add location targeting
- Optimize headlines

❌ Don’ts:
- Avoid broad keywords
- Don’t ignore negative keywords

🧠 Headlines:
1. Best {product} Near You
2. Affordable Plans
3. Join Today
4. Exclusive Offer
5. Start Now

🔥 Keywords:
{product}, best {product}, {product} near me

⚠️ Disclaimer:
Prices may vary by location

📌 Pin:
Visit website now
"""


    # ===============================
    # YOUTUBE SHORTS AGENT
    # ===============================
    def youtube_short_agent():
        return f"""
🎥 YOUTUBE SHORTS

🎯 Strategy:
- Hook in first 2 seconds
- Fast edits + energy

📈 Growth Plan:
- Post daily
- Follow trends
- Use viral formats

✅ Do’s:
- Keep short (<30 sec)
- Add captions
- Use trending music

❌ Don’ts:
- Don’t make slow videos
- Don’t skip hook

🧠 Captions:
1. This will change your life
2. Watch till end
3. No excuses
4. Start today
5. You can do this

🔥 Hashtags:
#shorts #viral #youtube #fitness #growth

📌 Pin Comment:
Subscribe for more
"""


    # ===============================
    # YOUTUBE LONG AGENT
    # ===============================
    def youtube_long_agent():
        return f"""
📺 YOUTUBE LONG VIDEO

🎯 Strategy:
- Educational + storytelling
- 8–12 min videos

📈 Growth Plan:
- SEO titles
- Consistent uploads
- Build authority

✅ Do’s:
- Provide value
- Use strong thumbnails
- Add CTA

❌ Don’ts:
- Don’t make boring intros
- Don’t skip SEO

🧠 Captions:
1. Complete beginner guide
2. Avoid these mistakes
3. Step-by-step plan
4. Transform in 30 days
5. Start today

🔥 Hashtags:
#youtube #fitness #growth #marketing #india

⚠️ Disclaimer:
Consult expert before starting

📌 Pin Comment:
Comment PLAN to get full guide
"""


    # ===============================
    # ROUTING
    # ===============================
    if platform == "instagram":
        result = instagram_agent(product, audience)

    elif platform == "facebook ads":
        result = facebook_agent()

    elif platform == "google ads":
        result = google_agent()

    elif platform == "youtube shorts":
        result = youtube_short_agent()

    elif platform == "youtube long":
        result = youtube_long_agent()

    elif platform == "all":
        result = "\n\n".join([
            instagram_agent(),
            facebook_agent(),
            google_agent(),
            youtube_short_agent(),
            youtube_long_agent()
        ])

    else:
        return {"error": "Invalid platform"}

    return {"campaign": result}