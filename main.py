from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root check
@app.get("/")
def home():
    return {"message": "AI SaaS Multi-Agent Running 🚀"}

# Multi-agent generator
@app.post("/generate")
async def generate(data: dict):
    product = data.get("product")
    audience = data.get("audience")
    platform = data.get("platform")

    if not product or not audience or not platform:
        return {"error": "Missing input"}

    # Multi-agent logic
    def instagram_agent():
        return f"📸 Instagram Ad:\nBoost your {product} for {audience} with eye-catching reels!"

    def facebook_agent():
        return f"📘 Facebook Ad:\nPromote {product} to {audience} with targeted campaigns."

    def google_agent():
        return f"🔍 Google Ads:\nRun high-converting ads for {product} targeting {audience}."

    def youtube_short_agent():
        return f"🎬 YouTube Shorts:\nCreate viral short videos for {product} targeting {audience}."

    def youtube_long_agent():
        return f"📺 YouTube Long:\nCreate detailed video marketing for {product} targeting {audience}."

    result = ""

    if platform == "Instagram":
        result = instagram_agent()

    elif platform == "Facebook Ads":
        result = facebook_agent()

    elif platform == "Google Ads":
        result = google_agent()

    elif platform == "YouTube Shorts":
        result = youtube_short_agent()

    elif platform == "YouTube Long":
        result = youtube_long_agent()

    elif platform == "All Platforms":
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