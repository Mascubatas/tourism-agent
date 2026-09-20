# Travel Planner Chatbot

A local travel-planning chatbot with a self-contained HTML chat UI, powered by a FastAPI backend
calling an Azure AI Foundry (OpenAI-compatible) endpoint.

## Setup

1. Create a virtual environment (skip if `.venv` already exists):
   ```powershell
   python -m venv .venv
   ```
2. Install dependencies:
   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
3. Configure your `.env` file (copy from `.env.example` if needed) with your Azure AI Foundry values:
   ```
   AZURE_ENDPOINT=https://<your-resource>.services.ai.azure.com/openai/v1
   AZURE_DEPLOYMENT=gpt-5-mini
   AZURE_API_KEY=<your-api-key>
   ```
4. Run the server:
   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app:app --reload --port 8000
   ```
5. Open [http://localhost:8000](http://localhost:8000) in your browser.

## Deploying on Render

This repo includes a `render.yaml` blueprint, so Render can configure the service automatically.

1. Push this repo to GitHub (already done if you're reading this on GitHub).
2. In the [Render dashboard](https://dashboard.render.com), click **New > Blueprint**, pick this repo,
   and Render will detect `render.yaml` (a Python web service running
   `uvicorn app:app --host 0.0.0.0 --port $PORT`).
   - Alternatively, click **New > Web Service** manually and set:
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
3. Under the service's **Environment** tab, add these environment variables (never commit real values
   to the repo — `.env` is gitignored and Render only reads variables you set in its dashboard):
   - `AZURE_ENDPOINT` = `https://<your-resource>.services.ai.azure.com/openai/v1`
   - `AZURE_DEPLOYMENT` = your deployment name
   - `AZURE_API_KEY` = your Azure AI Foundry API key
4. Deploy. Render builds the app and serves it at the URL it assigns (e.g.
   `https://arequipa-travel-bot.onrender.com`).
5. After changing any environment variable in Render, use **Manual Deploy > Clear build cache & deploy**
   or just restart the service — Render does not auto-reload on env var changes, similar to the local
   `--reload` caveat below.

## Troubleshooting

1. **Changed `.env` but nothing changed** — `uvicorn --reload` watches `.py` files but **not** `.env`.
   After editing `.env`, fully stop the server (Ctrl+C) and restart the `uvicorn` command above.

2. **401 "Access denied due to invalid subscription key or wrong API endpoint"** — Azure rejected the
   request. Check the terminal log for the real exception (it's logged server-side via
   `logging.exception`), then verify that `AZURE_API_KEY` and `AZURE_ENDPOINT` exactly match your
   project's deployment page.

3. **Isolate backend errors from the browser/UI** — test the `/chat` endpoint directly with
   PowerShell:
   ```powershell
   Invoke-RestMethod -Uri http://localhost:8000/chat -Method Post -ContentType 'application/json' -Body '{"messages":[{"role":"user","content":"hi"}]}'
   ```
