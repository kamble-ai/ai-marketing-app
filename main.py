from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from groq import Groq
import os
import sqlite3
from dotenv import load_dotenv

# =========================
# DB
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
# ENV
# =========================
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# APP
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
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except:
        return "❌ AI Error"

# =========================
# AUTH
# =========================
@app.post("/signup")
def signup(data: dict):
    try:
        if data["password"] != data["confirm_password"]:
            return {"error": "Passwords do not match"}

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
        return {"error": "User already exists"}


@app.post("/login")
def login(data: dict):

    cursor.execute("""
    SELECT * FROM users WHERE username=? AND password=?
    """, (data["username"], data["password"]))

    user = cursor.fetchone()

    if user:
        return {"message": "Login successful"}
    else:
        return {"error": "Invalid credentials"}


# =========================
# AGENTS
# =========================
def build_prompt(platform, product, audience):
    return f"""
Create a HIGH-CONVERTING {platform} marketing plan.

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

def run_agent(platform, product, audience):
    return ai_generate(build_prompt(platform, product, audience))


# =========================
# GENERATE
# =========================
@app.post("/generate")
def generate(data: dict):

    product = data["product"]
    audience = data["audience"]
    platform = data["platform"]
    username = data["username"]

    if platform == "all":
        platforms = [
            "Instagram", "Facebook Ads",
            "Google Ads", "YouTube Shorts", "YouTube Long"
        ]
        result = "\n\n".join([
            run_agent(p, product, audience) for p in platforms
        ])
    else:
        result = run_agent(platform, product, audience)

    cursor.execute("""
    INSERT INTO history (username, product, audience, platform, result)
    VALUES (?, ?, ?, ?, ?)
    """, (username, product, audience, platform, result))

    conn.commit()

    return {"campaign": result}


# =========================
# HISTORY
# =========================
@app.get("/history/{username}")
def history(username: str):

    cursor.execute("""
    SELECT product, audience, platform, result FROM history WHERE username=?
    """, (username,))

    data = cursor.fetchall()
    return {"history": data}


# =========================
# FRONTEND
# =========================
@app.get("/")
def home():
    return FileResponse("index.html")