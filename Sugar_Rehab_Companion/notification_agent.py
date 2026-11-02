"""One agent tool fans out every coach escalation to email and push."""

from agents import Agent, RunContextWrapper, function_tool
from notification_client import send_coach_notifications


@function_tool
async def notify_coach(ctx: RunContextWrapper[dict], subject: str, html: str, message: str) -> dict[str, str]:
    """Notify the coach by email and Pushover with HTML and plain-text summaries."""
    return await send_coach_notifications(ctx.context, subject, html, message)


notification_agent = Agent(
    name="Coach Notification Agent",
    instructions="""Use notify_coach once to notify the human coach through BOTH email
and Pushover. Choose subject and html for a professional, readable HTML email.
Choose a concise plain-text message of at most 1024 characters for the push alert.
Keep subject at most 250 characters. Summarize only facts provided by the user and
ask the coach to contact them. Email goes only to willowsayswhat@gmail.com; push
goes to the configured Pushover recipient. Report each channel's actual result.
Never claim delivery on failure or uncertainty. Do not retry or reply to the user.""",
    tools=[notify_coach],
    model="gpt-4o-mini",
)
