# Rehab-Coach-Bot

## Table of Contents
* [How to run this program](setup.md)
* [What is this app?](#what-is-this-app)
* [How it works](#how-it-works)
* [Agents](#agents)

---
# Version 0.0.2 (Branch) Improvements.

The 3rd iteration of the coach bot. We are now going to focus on improving the agents.

**We want to implement memory!**

but first..

*Still on the list* **FIXED** The moderation agent is replying to the user when the output is printed to the screen. We need to reword the system prompt to only get an "email send: summary - " kind of return. here is an example of what we are getting right now - **shift to object:** we are using structured output instead of a paragraph reply. It should now say "moderation done: No action taken. Or Email sent. 

**Reply Agent** *FIXED* is a helpful assistant. This won't cut it. We need to change the prompt to reflect an addiction coach. This was discovered by a simple "I ate sugar". While the moderator bot did its job and sent an alert to the human coach, the relpy bot replyed with:
```txt
It sounds like you enjoyed some sweet treats! Do you have a favorite dessert you like to indulge in?
```
This is unacceptable. So we will need to change the prompt to prevent this.

*make the router agent cheaper* We want to install Ollama to offset token spend. The Router agent only need to decide 2 things:
1. Is the message just general introductions? "hi", "I'm okay".
2. do we need a web search.


This can be achieved with a local model. Chit-chat doesn't need complete moderation. 

In fact, we might need to rethink how the router agent, and the `run()` workflow is spending tokens. 

**Fixed:** We added moderation to the GREETING OR SMALL TALK as this would have missed possible warning signs in the chat. 
**New problem** But now we are looking at ways to make sure we are not moderating "hello" as mentioned above. Spending tokens on small talk seems silly.

## What is this app?

Welcome to the **Sugar Rehab Companion**. It is a coachbot that lets the user chat about sugar and withdrawal from it. The app automates the interaction with the user: it answers questions, helps with actions, and supports a positive outlook during rehab. The chatbot also moderates the user's input for signs of distress or risk and can contact a human coach via email with a request for intervention.

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
    Email[Emailer agent]
    Search[Web search agent]
    ReplyWithResults[Reply agent with search results]
    Stream[Stream reply to user]

    UserMsg --> Router
    Router -->|No: greeting or small talk
    Router -->|Yes: needs research| Plan
    SimpleReply --> Stream
    Plan --> Moderate
    Moderate -->|False: Email not already sent| Email
    Moderate --> Search
    Search --> ReplyWithResults
    ReplyWithResults --> Stream
```

**Full pipeline (when research is needed):**

1. **Router** — Decides whether the message needs a web search. Greetings and small talk skip to a short reply.
2. **Planning** — The **Planner agent** turns the query into a small set of web search queries (e.g. two) aimed at supporting sugar rehab.
3. **Moderation** — The user’s message is assessed on a 1–6 scale. Depending on the level, the moderator either continues the flow, steers the user to positive content, or hands off to the **Email agent** to notify the coach.
4. **Search** — The **Web search agent** runs each planned query and returns short, factual summaries.
5. **Reply** — The **Reply agent** combines the user’s query and the search results into one helpful answer (and optional follow-up questions), which is streamed back to the user.

The UI streams status updates (e.g. “Got it!”, “Giving you the best answer…”, “Formatting my reply…”) and then the final reply. Traces can be viewed in the OpenAI dashboard for debugging.

---

## Agents

### Moderator agent

Listens to the user’s message and places it on a 1–6 scale of engagement and risk:

- **1–2** — General life or sugar-related chat; no escalation. The conversation continues and the rest of the pipeline runs (plan → search → reply).
- **3** — User is asking for ways to add sugar or similar; the moderator steers toward positive content (e.g. success stories).
- **4–6** — Frustration, desire to give up, or confession of having consumed sugar; the moderator **hands off to the Email agent** so the coach gets one email with a short subject and detailed body. A guard in the Email agent limits this to one email per run.

The moderator does not answer the user directly; it decides whether to escalate and then the main flow (planner → search → reply) still runs to produce the chat response.

### Email agent

Used only when the **Moderator agent** hands off (scale 4–6). It has a single tool, `send_email(subject, body)`, and sends one HTML email to the coach (via SendGrid). The agent is instructed to send one well-formatted email with a clear subject and body. A boolean guard prevents sending more than one email per session.

### Planner agent

Takes the user’s raw query and returns a **WebSearchPlan**: a list of search items (e.g. two), each with a `query` (search string) and a `reason` (why it helps). The instructions stress that the user is in sugar rehab, so planned searches should support quitting sugar and staying motivated rather than encouraging use.

### Web search agent

Has access to a **WebSearchTool** (web search API). Given a search term (and reason), it returns a concise 2–3 paragraph summary (under 300 words), focused on facts for a downstream synthesizer. The companion runs this agent once per planned search and collects the summaries.

### Reply agent

Receives the **user’s query** and the **list of web search result strings**. It produces a structured **ReplyToUser**: a single `reply` (the main answer) and optional `follow_up_questions`. The reply is helpful and informative, uses the search results, and keeps headings to the first three. This reply is what the user sees in the chat UI.
