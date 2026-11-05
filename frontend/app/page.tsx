"use client";

import { useEffect, useRef, useState } from "react";
import Markdown from "react-markdown";

type Message = { role: "user" | "assistant"; text: string };

const prompts = [
  "How can I handle an afternoon craving?",
  "Help me reflect on how today went.",
  "Where should I start with reducing sugar?",
];

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const end = useRef<HTMLDivElement>(null);
  const input = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    end.current?.scrollIntoView({ block: "end" });
  }, [messages, busy, error]);

  async function send() {
    const message = draft.trim();
    if (!message || busy) return;
    setDraft("");
    setError("");
    setBusy(true);
    setMessages((previous) => [...previous, { role: "user", text: message }]);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      if (!response.ok) throw new Error("Chat request failed");
      const { reply } = await response.json();
      if (typeof reply !== "string" || !reply.trim()) throw new Error("Empty reply");
      setMessages((previous) => [...previous, { role: "assistant", text: reply }]);
    } catch {
      setMessages((previous) => previous.slice(0, -1));
      setDraft(message);
      setError("The coach couldn’t reply. Your message is ready to resend.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="shell">
      <header>
        <span className="mark" aria-hidden="true">✳</span>
        <div><strong>Sugar Rehab Companion</strong><small>Personal coaching chat</small></div>
      </header>

      <section className="conversation" aria-label="Conversation" role="log">
        {!messages.length && (
          <div className="welcome">
            <p className="eyebrow">YOUR CHECK-IN</p>
            <h1>How are things going today?</h1>
            <p>Talk through a craving, reflect on your day, or plan your next small step.</p>
            <div className="prompts">
              {prompts.map((prompt) => (
                <button key={prompt} type="button" onClick={() => {
                  setDraft(prompt);
                  input.current?.focus();
                }}>{prompt}</button>
              ))}
            </div>
          </div>
        )}
        {messages.map(({ role, text }, index) => (
          <article key={index} className={`message ${role}`}>
            <small>{role === "user" ? "You" : "Companion"}</small>
            {role === "assistant" ? <Markdown>{text}</Markdown> : <p>{text}</p>}
          </article>
        ))}
        {busy && <p className="status" role="status">The coach is working on your reply…</p>}
        <div ref={end} />
      </section>

      <form onSubmit={(event) => { event.preventDefault(); void send(); }}>
        {error && <p className="error" role="alert">{error}</p>}
        <label htmlFor="message">Your message</label>
        <div className="composer">
          <textarea id="message" ref={input} rows={2} maxLength={4000}
            value={draft} readOnly={busy} placeholder="What’s on your mind?"
            onChange={(event) => setDraft(event.target.value)} />
          <button type="submit" disabled={busy || !draft.trim()}>Send <span aria-hidden="true">↑</span></button>
        </div>
      </form>
    </main>
  );
}
