"""Agent responsible for notifying the coach through Pushover."""

import asyncio

from agents import Agent, RunContextWrapper, function_tool
from pushover_client import send_push_notification


@function_tool
async def notify_coach(ctx: RunContextWrapper[dict], title: str, message: str) -> str:
    """Send one coach push alert with a short title and a plain-text summary."""
    if ctx.context.get("coach_notification_attempted"):
        return "A coach notification was already attempted during this moderation run. Do not send again."
    ctx.context["coach_notification_attempted"] = True
    return await asyncio.to_thread(send_push_notification, title, message)


pushover_agent = Agent(
    name="Pushover Notification Agent",
    instructions="""Notify the human coach about the user's situation using notify_coach once.
Use a professional plain-text title (at most 250 characters) and a concise factual
summary (at most 1024 characters), asking the coach to contact the user.
Include only relevant details supplied by the user. Do not reply to the user.
Report the tool's actual result. Do not claim delivery if the tool reports failure
or uncertainty, and do not retry within this run.""",
    tools=[notify_coach],
    model="gpt-4o-mini",
)
