from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# -------------------------
# FAKE DATABASE (in-memory)
# -------------------------
users = {}

# -------------------------
# MODELS
# -------------------------
class User(BaseModel):
    user_id: str
    languages: list[str]
    fluency: dict  # e.g. {"spanish": "fluent"}

class Submission(BaseModel):
    user_id: str
    language: str
    answer: str

# -------------------------
# TASK BANK (simple demo data)
# -------------------------
tasks = {
    "spanish": [
        {"question": "Translate: Hello, how are you?"},
        {"question": "What does 'gracias' mean?"}
    ],
    "somali": [
        {"question": "Translate: Good morning"},
        {"question": "What does 'ma fiicantahay' mean?"}
    ]
}

# -------------------------
# REGISTER USER
# -------------------------
@app.post("/register")
def register(user: User):
    users[user.user_id] = {
        "languages": user.languages,
        "fluency": user.fluency,
        "score": {lang: 0 for lang in user.languages},
        "points": 0
    }

    return {"message": "User registered", "data": users[user.user_id]}

# -------------------------
# GET TASK
# -------------------------
@app.get("/task/{user_id}/{language}")
def get_task(user_id: str, language: str):

    if language not in tasks:
        return {"error": "Language not supported yet"}

    task = random.choice(tasks[language])

    return {
        "user_id": user_id,
        "task": task
    }

# -------------------------
# SUBMIT ANSWER (SIMPLE SCORING)
# -------------------------
@app.post("/submit")
def submit(data: Submission):

    user = users.get(data.user_id)

    if not user:
        return {"error": "User not found"}

    # VERY SIMPLE "AI-like" scoring logic
    keywords = ["hello", "good", "morning", "thanks", "gracias", "fiican"]

    score = 0
    for word in keywords:
        if word in data.answer.lower():
            score += 1

    # update user score
    current = user["score"].get(data.language, 0)
    user["score"][data.language] = current + score

    # add points
    user["points"] += score * 10

    # confidence calculation
    confidence = min(100, user["score"][data.language] * 10)

    return {
        "score": score,
        "confidence": confidence,
        "total_points": user["points"]
    }

# -------------------------
# USER PROFILE
# -------------------------
@app.get("/profile/{user_id}")
def profile(user_id: str):
    return users.get(user_id, {"error": "User not found"})

