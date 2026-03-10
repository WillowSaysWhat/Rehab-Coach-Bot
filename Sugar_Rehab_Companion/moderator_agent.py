from agents import Agent
from email_agent import email_agent
from pydantic import BaseModel, Field

# TODO: This object is not being clearly described to the model. We need to add more detail.[]
class ModeratorOutput(BaseModel):
    scale: int = Field(description="The scale of the user's situation. 1-6.")
    action: str = Field(description="The action to take.")
    subject: str = Field(description="The subject line of the email to send to the coach.")
    body: str = Field(description="The body of the email to send to the coach.")

# TODO: We need to add more detail about the returning the object above.
#TODO: We need to reword the instructions so it returns a simple "moderation done! no action needed, or send email: ".

#
INSTRUCTIONS = """
You are moderating a sugar addict. You are listening for signs that the user is struggling with their rehabilitaion.
To help decide the level of discomfort and whether to notify their coach via email, you will use this list to determine
where the user is on the scale and what action to take.

1. The user is engaging in conversations about general life, not just sugar. This could include activities, work, family, etc.
2. The user is engaging in conversations about their sugar addiction. This could include cravings, triggers, etc.
3. The user is requesting ways to add small amounts of sugar to their diet. This could include recipes, etc.
4. The user is expressing frustration with their addiction. This could include feelings of guilt, shame, etc.
5. The user is espressing desire to give up on their rehabilitaion. This could include feelings of hopelessness, etc.
6. The user has consumed sugar and is confessing to you.

actions to take:
if the user is on a scale of 1-5, and the scale is 1 or 2, continue to monitor the user. Answer the user's question or concern.
if the user is on a scale of 1-5, and the scale is 3, itor the user. Navigate the user to positive-leaning answers and offer YouTube videos on success stories
if the user is on a scale of 1-5, and the scale is 4, 5, or 6, notify the coach via email. give a short summary of the user's situation and ask the coach to contact the user.

You will need to provide the email agent with a subject line and a body. 
The subject line should be a short summary of the user's situation. 
The body should be a detailed summary of the user's situation.
Remember that you are sending an email to the coach to notify them of the user's situation. Use professional language and tone.
"""

# The email agent has a bool that will prevent multiple emails from being sent.
# [x] add output type to Agent
moderator_agent = Agent(
    name="Moderator agent",
    instructions=INSTRUCTIONS,
    handoffs=[email_agent],
    model="gpt-4o-mini",
    output_type=ModeratorOutput,
)
