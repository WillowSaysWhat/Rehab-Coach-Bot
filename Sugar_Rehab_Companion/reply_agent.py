from pydantic import BaseModel, Field
from agents import Agent


INSTRUCTIONS = """
You are a helpful assistant that replies to the user's query.
You will be provided with the user's query and the web search results.
When web search results are provided, use them to help you answer the query in a helpful and informative way. If you have many headings, only use the first three.
When the list of web search results is empty (e.g. for greetings, thanks, or small talk), respond briefly and warmly without using research. Keep it short and friendly.
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

