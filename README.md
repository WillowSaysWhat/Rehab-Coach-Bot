# Rehab-Coach-Bot

Coach escalations use the **Coach Notification Agent** to attempt both Resend email
and Pushover push notifications. Email goes only to `willowsayswhat@gmail.com`.
Set `RESEND_API_KEY`, `PUSHOVER_API_TOKEN`, and `PUSHOVER_USER_KEY` in the root `.env`.
Each channel is attempted once per moderation run, even if the other fails.
Separate provider results and Resend acceptance IDs are logged in the app console.

## Table of Contents
* [How to run this program](setup.md)
* [What is this app?](#what-is-this-app)
* [How it works](#how-it-works)
* [Agents](#agents)

---
# Version 0.0.3 (Branch) Improvements.

Now we want memory.




## What is this app?

Welcome to the **Sugar Rehab Companion**. It is a coachbot that lets the user chat about sugar and withdrawal from it. The app automates the interaction with the user: it answers questions, helps with actions, and supports a positive outlook during rehab. The chatbot also moderates the user's input for signs of distress or risk and can contact a human coach via Pushover push notification with a request for intervention.

The Rehab Coachbot is designed to be embedded in a paywall dashboard, similar to chatbots on product websites and government portals. While it is built to assist via conversation, further integrations and permissions could extend it to navigation and search within the dashboard.

---

## How it works

When the user sends a message in the chat UI (Gradio), the app first **routes** the message. If it’s a greeting or small talk (e.g. “hi”, “thanks”), the **Reply agent** answers briefly with no web search. If the message needs research (questions about sugar, cravings, or rehab), the app runs the full pipeline: **Planner** → **Moderator** → **Web search** → **Reply agent**, then streams the reply to the user.

```mermaid
flowchart TB
    UserMsg[User message]
    Router[Router: needs_web_search?]
    SimpleReply[Reply agent with empty results]
    Plan[Planner agent]
    Moderate[Moderator agent]
    Email[Pushover notification agent]
    Search[Web search agent]
    ReplyWithResults[Reply agent with search results]
    Stream[Stream reply to user]

    UserMsg --> Router
    Router -->|No: greeting or small talk
    Router -->|Yes: needs research| Plan
    SimpleReply --> Stream
    Plan --> Moderate
    Moderate -->|Coach alert needed| Email
    Moderate --> Search
    Search --> ReplyWithResults
    ReplyWithResults --> Stream
```

**Full pipeline (when research is needed):**

1. **Router** — Decides whether the message needs a web search. Greetings and small talk skip to a short reply.
2. **Planning** — The **Planner agent** turns the query into a small set of web search queries (e.g. two) aimed at supporting sugar rehab.
3. **Moderation** — The user’s message is assessed on a 1–6 scale. Depending on the level, the moderator either continues the flow, steers the user to positive content, or hands off to the **Coach Notification Agent** to notify the coach.
4. **Search** — The **Web search agent** runs each planned query and returns short, factual summaries.
5. **Reply** — The **Reply agent** combines the user’s query and the search results into one helpful answer (and optional follow-up questions), which is streamed back to the user.

The UI streams status updates (e.g. “Got it!”, “Giving you the best answer…”, “Formatting my reply…”) and then the final reply. Traces can be viewed in the OpenAI dashboard for debugging.

---

## Agents

### Moderator agent

Listens to the user’s message and places it on a 1–6 scale of engagement and risk:

- **1–2** — General life or sugar-related chat; no escalation. The conversation continues and the rest of the pipeline runs (plan → search → reply).
- **3** — User is asking for ways to add sugar or similar; the moderator steers toward positive content (e.g. success stories).
- **4–6** — Frustration, desire to give up, or confession of having consumed sugar; the moderator **hands off to the Coach Notification Agent** so the coach gets both an HTML email and a concise push alert. The tool allows one delivery attempt per moderation run.

The moderator does not answer the user directly; it decides whether to escalate and then the main flow (planner → search → reply) still runs to produce the chat response.

### Coach Notification Agent

Used when the **Moderator agent** hands off (scale 4–6). Its `notify_coach(subject, html, message)` tool attempts both Resend and Pushover concurrently. The agent chooses the email subject and HTML and a concise plain-text push summary. Email is fixed to `willowsayswhat@gmail.com`. Both channels share a guard allowing one attempt per moderation run, and return separate results. A later chat message may generate new alerts.

See [notification setup](setup.md#pushover-coach-notifications) for credentials.

### Planner agent

Takes the user’s raw query and returns a **WebSearchPlan**: a list of search items (e.g. two), each with a `query` (search string) and a `reason` (why it helps). The instructions stress that the user is in sugar rehab, so planned searches should support quitting sugar and staying motivated rather than encouraging use.

### Web search agent

Has access to a **WebSearchTool** (web search API). Given a search term (and reason), it returns a concise 2–3 paragraph summary (under 300 words), focused on facts for a downstream synthesizer. The companion runs this agent once per planned search and collects the summaries.

### Reply agent

Receives the **user’s query** and the **list of web search result strings**. It produces a structured **ReplyToUser**: a single `reply` (the main answer) and optional `follow_up_questions`. The reply is helpful and informative, uses the search results, and keeps headings to the first three. This reply is what the user sees in the chat UI.
