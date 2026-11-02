import asyncio
import io
import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs

from pushover_client import send_push_notification


class PushoverTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {
            "PUSHOVER_API_TOKEN": "test-token", "PUSHOVER_USER_KEY": "test-user",
            "PUSHOVER_DEVICE": "phone",
        })
        env.start()
        self.addCleanup(env.stop)

    @patch("pushover_client.urlopen")
    def test_success_and_encoded_payload(self, request):
        response = io.BytesIO(b'{"status":1}')
        response.status = 200
        request.return_value.__enter__.return_value = response
        self.assertIn("accepted", send_push_notification("Coach alert", "Cravings & guilt"))
        args, kwargs = request.call_args
        self.assertEqual(kwargs["timeout"], 10)
        self.assertEqual(args[0].full_url, "https://api.pushover.net/1/messages.json")
        self.assertEqual(parse_qs(args[0].data.decode()), {
            "token": ["test-token"], "user": ["test-user"], "device": ["phone"],
            "title": ["Coach alert"], "message": ["Cravings & guilt"],
        })

    @patch("pushover_client.urlopen")
    def test_invalid_input_does_not_send(self, request):
        for title, message in [("", "body"), ("title", " "), ("x" * 251, "body"), ("title", "x" * 1025)]:
            self.assertIn("not sent", send_push_notification(title, message))
        with patch.dict(os.environ, {"PUSHOVER_API_TOKEN": ""}):
            self.assertIn("PUSHOVER_API_TOKEN", send_push_notification("title", "body"))
        request.assert_not_called()

    @patch("pushover_client.urlopen")
    def test_failures_do_not_report_success(self, request):
        for error in [URLError("offline"), TimeoutError(), HTTPError("url", 429, "quota", {}, None)]:
            request.side_effect = error
            self.assertNotIn("accepted", send_push_notification("title", "body"))
        request.side_effect = None
        for data in [b'{"status":0}', b'not json', b'[]']:
            response = io.BytesIO(data)
            response.status = 200
            request.return_value.__enter__.return_value = response
            self.assertNotIn("accepted", send_push_notification("title", "body"))

    def test_agent_guard_is_scoped_to_run(self):
        from agents import RunContextWrapper
        from pushover_agent import notify_coach

        async def check():
            context = RunContextWrapper(context={})
            with patch("pushover_agent.send_push_notification", return_value="accepted") as send:
                await notify_coach.on_invoke_tool(context, '{"title":"Title","message":"Body"}')
                result = await notify_coach.on_invoke_tool(context, '{"title":"Title","message":"Body"}')
                self.assertIn("already attempted", result)
                self.assertEqual(send.call_count, 1)
                await notify_coach.on_invoke_tool(RunContextWrapper(context={}), '{"title":"Title","message":"Body"}')
                self.assertEqual(send.call_count, 2)
        asyncio.run(check())


if __name__ == "__main__":
    unittest.main()
