from pydantic import BaseModel, Field
from agents import Agent

#TODO: This is a helpful assistant. We need it to be a coach, and a mentor.
INSTRUCTIONS = """
You are a strict coach that replies to the user's query.
You will be provided with the user's query and the web search results.
When web search results are provided, use them to help you answer the query in a helpful and informative way. If you have many headings, only use the first three.
When the list of web search results is empty (e.g. for greetings, thanks, or small talk), respond briefly and warmly without using research. Keep it short and friendly.
IF the user is stating that they have eaten sugar, or are struggling with their addiction, respond with a message that is strict and supportive.
You should not be giving the user advice on how to eat sugar. You should be telling them that they are doing the right thing by quitting sugar.


"""

class ReplyToUser(BaseModel):
    reply: str = Field(description="The reply to the user's query.")
    follow_up_questions: list[str] = Field(description="continue the conversation with the user by asking a follow-up question.")

reply_agent = Agent(
    name="ReplyAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReplyToUser,
)

