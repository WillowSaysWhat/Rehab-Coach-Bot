from agents import Runner, trace, gen_trace_id
from moderator_agent import moderator_agent
from web_search_agent import web_search_agent
from planner_agent import planner_agent, WebSearchPlan, WebSearchItem
from reply_agent import reply_agent
from moderator_agent import moderator_agent
import asyncio

class SugarRehabCompanion:
        
    async def run(self, query: str):
        """ Run the sugar rehab companion process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Sugar Rehab Companion trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting sugar rehab companion...")
            web_search_plan = await self.plan_searches(query) # returns WebSearchPlan object
            moderated_query = await self.moderate_query(query) # returns string
            print(f"Moderated query: {moderated_query}")
            yield("Got it! Giving you the best answer I can Find... This may take a 15 seconds or so...")
            web_search_results = await self.perform_searches(web_search_plan) # returns list of strings
            yield "Alright, Just formatting my reply... Gimme a sec..."
            answer = await self.reply_to_user(query, web_search_results) # returns ReplyToUser object   
            yield(answer.reply)
            
            
    async def plan_searches(self, query: str):
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(planner_agent, f"Query: {query}")
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)
    
    async def perform_searches(self, search_plan: WebSearchPlan):
        """ Perform the searches to perform for the query """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem):
        """ Perform a search for the query """
        print(f"Searching for {item.query}...")
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                web_search_agent,
            )
            return str(result.final_output)
        except Exception:
            return None
        
    async def reply_to_user(self, query: str, web_search_results: list[str]):
        """ Reply to the user's query """
        print("Replying to user...")
        result = await Runner.run(reply_agent, f"Query: {query}\nWeb search results: {web_search_results}")
        return result.final_output_as(str)
    
    async def moderate_query(self, query: str):
        """ Moderate the query """
        print("Moderating query...")
        result = await Runner.run(moderator_agent, f"Query: {query}")
        return result.final_output_as(str)