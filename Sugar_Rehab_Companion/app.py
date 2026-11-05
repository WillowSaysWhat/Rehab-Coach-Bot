import os
from secrets import compare_digest

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from sugar_rehab_companion import SugarRehabCompanion

load_dotenv()

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(body: ChatRequest, authorization: str = Header(default="")):
    token = os.getenv("COACH_API_TOKEN")
    if not token:
        raise HTTPException(status_code=503, detail="Chat service is not configured.")
    if not compare_digest(authorization.encode(), f"Bearer {token}".encode()):
        raise HTTPException(status_code=401, detail="Unauthorized.")

    message = body.message.strip()
    if not message or len(message) > 4000:
        raise HTTPException(status_code=400, detail="Enter a message of 1 to 4,000 characters.")

    reply = "".join([chunk async for chunk in SugarRehabCompanion().run(message)])
    if not reply.strip():
        raise HTTPException(status_code=502, detail="The coach returned an empty reply.")
    return {"reply": reply}
