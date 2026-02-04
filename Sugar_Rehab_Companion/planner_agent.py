from pydantic import BaseModel, Field
from agents import Agent

HOW_MANY_SEARCHES = 2

INSTRUCTIONS = """
You are a helpful research assistant. Given a query, come up with a set of web searches to perform to best answer the query.
Output {HOW_MANY_SEARCHES} terms to query for. The queries should be specific to the query and should be relevant to the query.
You will need to use the user's answers to the clarifying questions to refine the queries. Focus on giving information 
that reinforces the user's determination to quit sugar. 
It is important to note that the user is a sugar addict and is struggling with their addiction.
"""

# web search query with the reason why the query is important to the query.
class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")
    
# list of web search queries - which should have 2 queries for now
class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
    
)


    