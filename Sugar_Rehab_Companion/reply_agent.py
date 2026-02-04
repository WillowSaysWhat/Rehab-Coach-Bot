from pydantic import BaseModel, Field
from agents import Agent


INSTRUCTIONS = """
You are a helpful assistant that replies to the user's query.
You will be provided with the user's query and the web search results.
You should reply to the user's query in a way that is helpful and informative.
You should use the web search results to help you answer the query.
You should reply in a way that is helpful and informative.
If you have many headings, only use the first three.
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

