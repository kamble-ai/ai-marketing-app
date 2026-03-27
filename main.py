from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
import os
import sqlite3
from dotenv import load_dotenv

# =========================
# DATABASE SETUP
# =========================
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    product TEXT,
    audience TEXT,
    platform TEXT,
    result TEXT
)
""")

conn.commit()

# =========================
# LOAD ENV
# =========================
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# FASTAPI INIT
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MODELS
# =========================
class User(BaseModel):
    username: str
    password: str

class GenerateRequest(BaseModel):
    username: str
    product: str
    audience: str
    platform: str

# =========================
# AI FUNCTION
# =========================
def ai_generate(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# =========================
# AUTH ROUTES
# =========================
@app.post("/signup")
def signup(user: User):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))
        conn.commit()
        return {"message": "User created"}
    except:
        raise HTTPException(status_code=400, detail="User already exists")

@app.post("/login")
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, user.password))
    result = cursor.fetchone()
    if result:
        return {"message": "Login success"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# =========================
# AGENTS
# =========================
def instagram_agent(product, audience):
    prompt = f"""
Create a HIGH-CONVERTING Instagram marketing plan.

Product: {product}
Audience: {audience}

Give:
1. Strategy
2. Growth Plan
3. Do's & Don'ts
4. 5 Captions
5. Hashtags
6. CTA
"""
    return ai_generate(prompt)

def facebook_agent(product, audience):
    prompt = f"""
Create Facebook Ads strategy.

Product: {product}
Audience: {audience}

Include strategy, captions, hashtags, CTA.
"""
    return ai_generate(prompt)

def google_agent(product, audience):
    prompt = f"""
Create Google Ads campaign.

Product: {product}
Audience: {audience}

Include keywords, headlines, strategy.
"""
    return ai_generate(prompt)

def youtube_short_agent(product, audience):
    prompt = f"""
Create YouTube Shorts strategy.

Product: {product}
Audience: {audience}

Include hook, captions, hashtags.
"""
    return ai_generate(prompt)

def youtube_long_agent(product, audience):
    prompt = f"""
Create YouTube long video plan.

Product: {product}
Audience: {audience}

Include SEO, titles, strategy.
"""
    return ai_generate(prompt)

# =========================
# GENERATE ROUTE
# =========================
@app.post("/generate")
def generate(data: GenerateRequest):

    product = data.product
    audience = data.audience
    platform = data.platform.lower()
    username = data.username

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
        raise HTTPException(status_code=400, detail="Invalid platform")

    # SAVE HISTORY
    cursor.execute(
        "INSERT INTO history (username, product, audience, platform, result) VALUES (?, ?, ?, ?, ?)",
        (username, product, audience, platform, result)
    )
    conn.commit()

    return {"campaign": result}

# =========================
# HISTORY ROUTE
# =========================
@app.get("/history/{username}")
def get_history(username: str):
    cursor.execute("SELECT product, audience, platform, result FROM history WHERE username=?", (username,))
    data = cursor.fetchall()
    return {"history": data}

# =========================
# FRONTEND
# =========================
@app.get("/")
def home():
    return FileResponse("index.html")