from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from groq import Groq
import os
import sqlite3
from dotenv import load_dotenv

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    dob TEXT,
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
# ENV + GROQ
# =========================
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# FASTAPI
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
# AI FUNCTION
# =========================
def ai_generate(prompt):
    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

    for model in models:
        try:
            res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return res.choices[0].message.content
        except Exception as e:
            print(model, "failed", e)

    return "❌ AI failed"

# =========================
# AUTH
# =========================
@app.post("/signup")
def signup(data: dict):
    if data["password"] != data["confirm_password"]:
        return {"error": "Passwords do not match"}

    try:
        cursor.execute("""
        INSERT INTO users (first_name, last_name, gender, dob, username, password)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["first_name"],
            data["last_name"],
            data["gender"],
            data["dob"],
            data["username"],
            data["password"]
        ))
        conn.commit()
        return {"message": "Account created successfully"}
    except:
        return {"error": "Username already exists"}

@app.post("/login")
def login(data: dict):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )
    if cursor.fetchone():
        return {"message": "Login successful"}
    return {"error": "Invalid login"}

# =========================
# AGENTS
# =========================
def instagram_agent(p, a):
    return ai_generate(f"""
Create a HIGH-CONVERTING Instagram marketing plan.

Product: {p}
Audience: {a}

Give:
1. Strategy
2. Content Plan
3. Growth Plan
4. Captions
5. Hashtags
6. CTA
""")

def facebook_agent(p, a):
    return ai_generate(f"""
Create Facebook Ads strategy.

Product: {p}
Audience: {a}

Include targeting, ad copy, headlines, budget, CTA.
""")

def google_agent(p, a):
    return ai_generate(f"""
Create Google Ads campaign.

Product: {p}
Audience: {a}

Include keywords, headlines, SEO, bidding strategy.
""")

def youtube_short_agent(p, a):
    return ai_generate(f"""
Create YouTube Shorts strategy.

Product: {p}
Audience: {a}

Include hook, script, captions, hashtags.
""")

def youtube_long_agent(p, a):
    return ai_generate(f"""
Create YouTube long video plan.

Product: {p}
Audience: {a}

Include SEO title, script, thumbnail idea.
""")

def all_platform_agent(p, a):
    return ai_generate(f"""
Create COMPLETE marketing strategy.

Product: {p}
Audience: {a}

Include:
Instagram + Facebook + Google + YouTube
+ Content calendar + Growth strategy
""")

# =========================
# GENERATE
# =========================
@app.post("/generate")
def generate(data: dict):

    p = data["product"]
    a = data["audience"]
    platform = data["platform"].lower()
    u = data["username"]

    if platform == "instagram":
        result = instagram_agent(p, a)
    elif platform == "facebook ads":
        result = facebook_agent(p, a)
    elif platform == "google ads":
        result = google_agent(p, a)
    elif platform == "youtube shorts":
        result = youtube_short_agent(p, a)
    elif platform == "youtube long":
        result = youtube_long_agent(p, a)
    elif platform == "all":
        result = all_platform_agent(p, a)
    else:
        return {"error": "Invalid platform"}

    cursor.execute(
        "INSERT INTO history (username, product, audience, platform, result) VALUES (?, ?, ?, ?, ?)",
        (u, p, a, platform, result)
    )
    conn.commit()

    return {"campaign": result}

# =========================
# HISTORY
# =========================
@app.get("/history/{username}")
def history(username: str):
    cursor.execute(
        "SELECT product, platform, result FROM history WHERE username=?",
        (username,)
    )
    return {"history": cursor.fetchall()}

# =========================
# FRONTEND
# =========================
@app.get("/")
def home():
    return FileResponse("index.html")