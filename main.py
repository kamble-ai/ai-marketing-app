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
    return FileResponse("index.html")


# =========================
# MULTI-AGENT GENERATOR
# =========================
@app.post("/generate")
async def generate(data: dict):
    product = data.get("product")
    audience = data.get("audience")
    platform = data.get("platform")

    # Validation
    if not product or not audience or not platform:
        return {"error": "Missing input"}

    # Normalize input (VERY IMPORTANT)
    platform = platform.lower()

    # =========================
    # AGENTS
    # =========================

    def instagram_agent():
        return f"""📸 Instagram Ad:
Boost your {product} for {audience} with eye-catching reels and viral content.
Use trending audio + strong CTA like “Join Now!”"""

    def facebook_agent():
        return f"""📘 Facebook Ad:
Promote {product} to {audience} with targeted campaigns.
Use detailed descriptions, testimonials, and retargeting ads."""

    def google_agent():
        return f"""🔍 Google Ads:
Run high-converting ads for {product} targeting {audience}.
Focus on keywords, search intent, and landing page optimization."""

    def youtube_short_agent():
        return f"""🎬 YouTube Shorts:
Create viral short videos for {product} targeting {audience}.
Hook in first 3 seconds + fast cuts + captions."""

    def youtube_long_agent():
        return f"""📺 YouTube Long Video:
Create detailed video marketing for {product} targeting {audience}.
Include storytelling, problem-solution format, and CTA."""

    # =========================
    # ROUTING LOGIC
    # =========================

    if platform == "instagram":
        result = instagram_agent()

    elif platform == "facebook_ads":
        result = facebook_agent()

    elif platform == "google_ads":
        result = google_agent()

    elif platform == "youtube_short":
        result = youtube_short_agent()

    elif platform == "youtube_long":
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