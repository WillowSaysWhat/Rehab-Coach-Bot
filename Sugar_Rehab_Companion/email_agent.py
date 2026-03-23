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
    
    """send an Email with the given subject and HTML body."""
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    from_email = Email("willowsayswhat@gmail.com")
    to_email = To("willowsayswhat@gmail.com")
    content = Content("text/html", body)
    mail = Mail(from_email, to_email, subject, content).get()
    print( "Sending email..." )
    response = sg.client.mail.send.post(request_body=mail)
    print (f"Email sent: {response.status_code}")
    return "successfully sent email"
#NOTE: This is the instructions that decides the tone of the email.
INSTRUCTIONS = """ You are a professional email agent in a sugar addiction rehabilitaion program.
You are able to send a nicely formatted email. 
You should use your tool to send one email to the coach, providing a subject and body.
The subject should be a short summary of the user's situation.
The body should be a detailed summary of the user's situation.
Use professional language and tone.
Remember that you are sending an email to the coach. Don't send a reply to the user. Notify the coach about the user's situation.
Here is an example of an email to the coach:
Subject: User is struggling with their addiction
Body: The user is struggling with their addiction. They are expressing feelings of hopelessness and desire to give up on their rehabilitaion. They have consumed sugar and are confessing to you.
"""

email_agent = Agent(
    name="Email Agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
    
)