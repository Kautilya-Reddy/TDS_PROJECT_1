# LLM Code Deployment - Student API

This project is part of the **Tools in Data Science (TDS)** course at **IIT Madras BS in Data Science**.

It implements a **FastAPI-based API** that receives JSON requests describing an app specification, generates and deploys a web app to **GitHub Pages**, and returns the deployment details to the evaluator for automated assessment.

---

## 🚀 Features

- Accepts JSON POST requests at `/task`
- Verifies secret keys provided by IITM evaluators
- Uses a GitHub personal access token to:
  - Create a public repository
  - Upload files (`index.html`, `README.md`, `LICENSE`, etc.)
  - Enable GitHub Pages deployment
- Returns:
  - `repo_url` → GitHub repository link  
  - `commit_sha` → Commit ID  
  - `pages_url` → Deployed web app link

---

## 🧠 Example Request

```bash
curl -X POST https://<your-app-name>.onrender.com/task \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "secret": "mysecret123",
    "task": "github-user-created",
    "round": 1,
    "nonce": "abc123",
    "brief": "Bootstrap GitHub lookup app",
    "attachments": [],
    "checks": [],
    "evaluation_url": "https://example.com/notify"
  }'
