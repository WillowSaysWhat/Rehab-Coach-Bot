from agents import Agent, function_tool
from resend_client import send_email


@function_tool
def email_tool(subject: str, html: str) -> str:
    """Send an email only to the coach with an agent-written subject and HTML."""
    return send_email(subject, html)


#NOTE: This is the instructions that decides the tone of the email.
INSTRUCTIONS = """ You are a professional email agent in a sugar addiction rehabilitaion program.
You are able to send a nicely formatted email. 
Use email_tool once to send an email to the coach at willowsayswhat@gmail.com.
Choose the subject and html arguments yourself based on the user's situation.
Format html as a readable HTML email. The recipient and sender are fixed by the tool.
Report the tool's actual result; do not claim success on failure or retry an uncertain send.
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
    tools=[email_tool],
    model="gpt-4o-mini",
    
)
