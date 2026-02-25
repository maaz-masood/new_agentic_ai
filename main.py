import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Body
from pydantic import BaseModel
from agents import Agent, Runner
from email_tools import send_email_raw

load_dotenv(r"C:\Users\owner\projects\agents\.env", override=True)

app = FastAPI()

reply_agent = Agent(
    name="EmailResponder",
    instructions="Reply politely and professionally to incoming emails.",
    model="gpt-4o-mini",
)

class InboundEmail(BaseModel):
    from_: str = ""
    subject: str = ""
    text: str = ""

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/inbound-email")
async def inbound_email(
    request: Request,
    payload: InboundEmail | None = Body(default=None),
):
    # 1) Swagger/JSON path (gives you fields in /docs)
    if payload is not None:
        sender = payload.from_.strip()
        subject = payload.subject
        body = payload.text
    else:
        # 2) SendGrid inbound parse path (form-data)
        form = await request.form()
        data = dict(form)
        sender = (data.get("from") or "").strip()
        subject = data.get("subject", "")
        body = data.get("text") or data.get("html") or ""

    # Dev-friendly: don’t 400 when you hit Execute with empty body
    if not sender:
        return {"status": "noop", "reason": "missing sender"}

    prompt = f"Reply to this email.\n\n{body}"
    result = await Runner.run(reply_agent, prompt)

    reply_text = result.final_output
    reply_subject = subject if subject.lower().startswith("re:") else f"Re: {subject}"

    code, _ = send_email_raw(to=sender, subject=reply_subject, body=reply_text)
    if code != 202:
        raise HTTPException(status_code=502, detail=f"SendGrid failed: {code}")

    return {"status": "replied", "reply": reply_text}
