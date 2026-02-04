import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

# variable that prevents multiple emails from being sent.
email_sent = False

@function_tool
def send_email(subject: str, body: str):
    #guard against multiple emails being sent.
    if email_sent:
        return "Email already sent"
    
    """send an with the given subject and HTML body."""
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    from_email = Email("willowsayswhat@gmail.com")
    to_email = To("willowsayswhat@gmail.com")
    content = Content("text/html", body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    return "successfully sent email"

INSTRUCTIONS = """ You are able to send a nicely formatted email. 
You should use your tool to send one email to the user, providing a subject and body.
"""

email_agent = Agent(
    name="Email Agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
    
)