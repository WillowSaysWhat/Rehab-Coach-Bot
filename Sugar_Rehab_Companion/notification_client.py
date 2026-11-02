"""Deliver each coach escalation through both configured channels."""

import asyncio
import logging
from pathlib import Path

from dotenv import load_dotenv
from pushover_client import send_push_notification
from resend_client import send_email

logger = logging.getLogger(__name__)


async def send_coach_notifications(context: dict, subject: str, html: str, message: str) -> dict[str, str]:
    """Attempt both channels once per run, including when one provider fails."""
    if context.get("coach_notification_attempted"):
        return {"status": "Coach notifications already attempted during this moderation run. Do not retry."}
    context["coach_notification_attempted"] = True
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    outcomes = await asyncio.gather(
        asyncio.to_thread(send_email, subject, html),
        asyncio.to_thread(send_push_notification, subject[:250], message),
        return_exceptions=True,
    )
    results = {}
    for channel, outcome in zip(("email", "pushover"), outcomes):
        if isinstance(outcome, BaseException):
            outcome = f"Delivery could not be confirmed ({type(outcome).__name__}). Do not retry."
        results[channel] = outcome
        logger.warning("Coach notification %s: %s", channel, outcome)
    return results
