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
