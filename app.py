from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import requests, json

from db import db, init_db
from generator import generate_app

app = FastAPI()
init_db()

STUDENT_SECRET = "mysecret123"  # Must match what evaluator sends

class TaskRequest(BaseModel):
    email: str
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    attachments: list
    checks: list
    evaluation_url: str


@app.get("/")
def home():
    return {"status": "ok", "message": "LLM App Deployment API is running."}


@app.post("/api-endpoint")
def receive_task(task: TaskRequest):
    print(f"📥 Received task: {task.task} (Round {task.round})")

    # Step 1: Verify secret
    if task.secret != STUDENT_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

    # Step 2: Generate and deploy app
    try:
        print("🚀 Generating and deploying app...")
        result = generate_app(task.task, task.brief)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"App generation failed: {e}")

    # Step 3: Log task locally in DB
    with db() as conn:
        conn.execute(
            """
            INSERT INTO tasks(timestamp, email, task, round, nonce, brief, attachments, checks, evaluation_url, endpoint, statuscode, secret)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                task.email,
                task.task,
                task.round,
                task.nonce,
                json.dumps(task.brief),
                json.dumps(task.attachments),
                json.dumps(task.checks),
                task.evaluation_url,
                "http://127.0.0.1:8001/task",
                200,
                task.secret,
            ),
        )

    # Step 4: Notify evaluator (evaluation_url)
    try:
        payload = {
            "email": task.email,
            "task": task.task,
            "round": task.round,
            "nonce": task.nonce,
            "repo_url": result["repo_url"],
            "commit_sha": result["commit_sha"],
            "pages_url": result["pages_url"],
        }

        response = requests.post(task.evaluation_url, json=payload)
        print(f"📤 Sent repo info to evaluator → Status: {response.status_code}")

        if response.status_code != 200:
            print("⚠️ Evaluator did not accept payload:", response.text)

    except Exception as e:
        print(f"❌ Failed to notify evaluator: {e}")

    return {
        "status": "success",
        "repo_url": result["repo_url"],
        "pages_url": result["pages_url"],
        "commit_sha": result["commit_sha"],
    }
