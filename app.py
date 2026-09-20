import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT")
AZURE_DEPLOYMENT = os.environ.get("AZURE_DEPLOYMENT")
AZURE_API_KEY = os.environ.get("AZURE_API_KEY")

SYSTEM_PROMPT = (
    "You are a friendly, well-traveled trip-planning expert who specializes in trips to Arequipa, Peru. "
    "You help people plan Arequipa trips - suggesting itineraries, things to do, rough budgeting, and "
    "packing tips - in clear, practical language tailored to their interests, budget, dates, and travel "
    "style. You help travelers estimate and compare airfare options (routes, typical price ranges, best "
    "times to book) and recommend the kinds of local guides or tour operators worth contacting for "
    "Arequipa (e.g. Colca Canyon treks, city tours, Misti climbs), including example contact details "
    "such as a business name, phone number, or email when helpful. You cannot actually book flights, "
    "tours, or guides yourself - you only suggest options. Ask clarifying questions when useful, such "
    "as who is going, the budget, the season, and the preferred pace. Always remind users to verify "
    "time-sensitive details themselves - visas, opening hours, prices, weather, flight availability, and "
    "any guide/operator contact details - since these change and you may not have current or accurate "
    "information. Be enthusiastic but realistic."
)

app = FastAPI()

client = None
if AZURE_ENDPOINT and AZURE_API_KEY:
    client = OpenAI(base_url=AZURE_ENDPOINT, api_key=AZURE_API_KEY)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


@app.get("/")
async def index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))


@app.post("/chat")
async def chat(request: ChatRequest):
    if not AZURE_ENDPOINT or not AZURE_DEPLOYMENT or not AZURE_API_KEY:
        logger.error(
            "Missing configuration: AZURE_ENDPOINT=%s, AZURE_DEPLOYMENT=%s, AZURE_API_KEY set=%s",
            bool(AZURE_ENDPOINT), bool(AZURE_DEPLOYMENT), bool(AZURE_API_KEY),
        )
        return JSONResponse(
            status_code=500,
            content={"error": "Server is missing required configuration (AZURE_ENDPOINT, AZURE_DEPLOYMENT, AZURE_API_KEY). Check the .env file."},
        )

    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend({"role": m.role, "content": m.content} for m in request.messages)

        completion = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=messages,
        )
        reply = completion.choices[0].message.content
        return {"reply": reply}
    except Exception:
        logger.exception("Error while calling the chat completion API")
        return JSONResponse(
            status_code=500,
            content={"error": "Sorry, I'm having trouble answering right now. Please try again in a moment."},
        )
