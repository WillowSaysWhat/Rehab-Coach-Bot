from agents import Agent
from notification_agent import notification_agent
from pydantic import BaseModel, Field

# TODO: This object is not being clearly described to the model. We need to add more detail.[x]


# TODO: We need to add more detail about the returning the object above.
#TODO: We need to reword the instructions so it returns a simple "moderation done! no action needed, or send email: ".

#
INSTRUCTIONS = """
You are moderating a sugar addict. You are listening for signs that the user is struggling with their rehabilitaion.
To help decide the level of discomfort and whether to notify their coach via email and Pushover, you will use this list to determine
where the user is on the scale and what action to take.

1. The user is engaging in conversations about general life, not just sugar. This could include activities, work, family, etc.
2. The user is engaging in conversations about their sugar addiction. This could include cravings, triggers, etc.
3. The user is requesting ways to add small amounts of sugar to their diet. This could include recipes, etc.
4. The user is expressing frustration with their addiction. This could include feelings of guilt, shame, etc.
5. The user is espressing desire to give up on their rehabilitaion. This could include feelings of hopelessness, etc.
6. The user has consumed sugar and is confessing to you.

actions to take:
if the user is on 1, 2 or 3, continue to monitor the user.
if the user is on 4, 5, or 6, notify the coach via email and Pushover. give a short summary of the user's situation and ask the coach to contact the user.

Provide the Coach Notification Agent with a subject, a readable HTML email,
and a concise plain-text push message (at most 1024 characters).
Hand off to that agent to notify the coach. Use professional language and tone.

Don't send a reply to the user. Notify the coach about the user's situation.
Here is an example of a notification to the coach:
Subject: User is struggling with their addiction
Body: The user is struggling with their addiction. They are expressing feelings of hopelessness and desire to give up on their rehabilitaion. They have consumed sugar and are confessing to you.
"""

# The shared notification tool allows one attempt per channel per moderation run.
# [x] add output type to Agent
moderator_agent = Agent(
    name="Moderator agent",
    instructions=INSTRUCTIONS,
    handoffs=[notification_agent],
    model="gpt-4o-mini",
    
)
