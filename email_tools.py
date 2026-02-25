import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from agents import function_tool

def send_email_raw(to: str, subject: str, body: str):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])
    from_email = Email(os.environ["VERIFIED_SENDER_EMAIL"])
    mail = Mail(from_email, To(to), subject, Content("text/plain", body)).get()
    resp = sg.client.mail.send.post(request_body=mail)
    return resp.status_code, resp.body

send_email_tool = function_tool(send_email_raw)  # only if you want the LLM to call it
