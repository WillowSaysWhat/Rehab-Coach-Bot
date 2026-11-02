import ast
import io
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from notification_client import send_coach_notifications


class NotificationTests(unittest.IsolatedAsyncioTestCase):
    async def test_both_provider_requests_are_executed(self):
        response = io.BytesIO(b'{"status":1}')
        response.status = 200
        with patch.dict(os.environ, {
            "RESEND_API_KEY": "test-key", "PUSHOVER_API_TOKEN": "test-token",
            "PUSHOVER_USER_KEY": "test-user",
        }), patch("resend_client.resend.Emails.send", return_value={"id": "test-email"}) as email, patch("pushover_client.urlopen") as push:
            push.return_value.__enter__.return_value = response
            result = await send_coach_notifications({}, "Coach alert", "<p>Summary</p>", "Summary")
            email.assert_called_once_with({
                "from": "onboarding@resend.dev", "to": "willowsayswhat@gmail.com",
                "subject": "Coach alert", "html": "<p>Summary</p>",
            })
            push.assert_called_once()
            self.assertIn("accepted", result["email"])
            self.assertIn("accepted", result["pushover"])

    async def test_each_channel_runs_even_when_other_raises(self):
        for failing in ("email", "pushover"):
            with self.subTest(failing=failing), patch("notification_client.send_email") as email, patch("notification_client.send_push_notification") as push:
                email.return_value = "Email accepted"
                push.return_value = "Push accepted"
                (email if failing == "email" else push).side_effect = RuntimeError("provider failure")
                result = await send_coach_notifications({}, "Title", "<p>Body</p>", "Body")
                email.assert_called_once()
                push.assert_called_once()
                self.assertIn("could not be confirmed", result[failing])
                self.assertIn("accepted", result["pushover" if failing == "email" else "email"])

    async def test_duplicate_guard_and_new_run(self):
        with patch("notification_client.send_email", return_value="Email failed") as email, patch("notification_client.send_push_notification", return_value="Push accepted") as push:
            context = {}
            await send_coach_notifications(context, "Title", "<p>Body</p>", "Body")
            duplicate = await send_coach_notifications(context, "Title", "<p>Body</p>", "Body")
            self.assertIn("already attempted", duplicate["status"])
            self.assertEqual(email.call_count, 1)
            self.assertEqual(push.call_count, 1)
            await send_coach_notifications({}, "Title", "<p>Body</p>", "Body")
            self.assertEqual(email.call_count, 2)
            self.assertEqual(push.call_count, 2)

    async def test_moderator_routes_to_combined_agent(self):
        from moderator_agent import moderator_agent
        from notification_agent import notification_agent

        self.assertEqual(moderator_agent.handoffs, [notification_agent])
        self.assertEqual([tool.name for tool in notification_agent.tools], ["notify_coach"])
        tree = ast.parse(Path(__file__).with_name("moderator_agent.py").read_text())
        handoffs = [kw.value for node in ast.walk(tree) if isinstance(node, ast.Call)
                    for kw in node.keywords if kw.arg == "handoffs"]
        self.assertEqual([n.id for n in handoffs[0].elts], ["notification_agent"])


if __name__ == "__main__":
    unittest.main()
