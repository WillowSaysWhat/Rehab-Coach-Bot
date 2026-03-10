from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = """
You classify whether the user's message requires a web search to answer well.

Set needs_web_search to True only if the user is asking for information, advice, or help about sugar, cravings, diet, lifestyle, or rehabilitation that would benefit from looking up current information.

Set needs_web_search to False for:
- Greetings (e.g. hi, hello, hey)
- Thanks, goodbye, or other small talk
- Simple social messages that do not ask for research or advice
"""


class NeedsWebSearch(BaseModel):
    needs_web_search: bool = Field(
        description="True if the message requires web search to answer; False for greetings, thanks, goodbye, or small talk."
    )

#TODO: Install Ollama and use it to run the router agent.
# we are using too many tokens with the gpt-4o-mini model to just check if the message requires a web search or moderation

router_agent = Agent(
    name="RouterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=NeedsWebSearch,
)
