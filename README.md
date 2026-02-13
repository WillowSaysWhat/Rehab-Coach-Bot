# Rehab-Coach-Bot

## Table of Contents
* [How to run this program](setup.md)
* [What is this app?](#what-is-this-app)
* [How it works](#how-it-works)
* [Agents](#agents)

---

<p align="center">
  <img src="interations_image.jpg" alt="Iterations Image" >
</p>

---

## What is this app?

Welcome to the **Sugar Rehab Companion**. It is a coachbot that lets the user chat about sugar and withdrawal from it. The app automates the interaction with the user: it answers questions, helps with actions, and supports a positive outlook during rehab. The chatbot also moderates the user's input for signs of distress or risk and can contact a human coach via email with a request for intervention.

NOTE: Email API (SendGrid) is on a user trial, so its functionality probably doesn't work right now.

The Rehab Coachbot is designed to be embedded in a paywall dashboard, similar to chatbots on product websites and government portals. While it is built to assist via conversation, further integrations and permissions could extend it to navigation and search within the dashboard.

---

## How it works

When the user sends a message in the chat UI (Gradio), the app runs a fixed pipeline:

1. **Moderation** — The user’s message is assessed on a 1–6 scale. Depending on the level, the moderator either continues the flow, steers the user to positive content, or hands off to the **Email agent** to notify the coach.
2. **Planning** — A **Planner agent** turns the user’s query into a small set of web search queries (e.g. two) aimed at supporting sugar rehab.
3. **Search** — A **Web search agent** runs each planned query and returns short, factual summaries.
4. **Reply** — A **Reply agent** combines the user’s query and the search results into one helpful answer (and optional follow-up questions), which is streamed back to the user.

The UI streams status updates (e.g. “Giving you the best answer…”, “Formatting my reply…”) and then the final reply. Traces can be viewed in the OpenAI dashboard for debugging.

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
