export const maxDuration = 300;

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const message = typeof body?.message === "string" ? body.message.trim() : "";
  if (!message || message.length > 4000) {
    return Response.json({ error: "Enter a message of 1 to 4,000 characters." }, { status: 400 });
  }

  const origin = process.env.COACH_API_URL;
  const token = process.env.COACH_API_TOKEN;
  if (!origin || !token) {
    return Response.json({ error: "Chat service is not configured." }, { status: 503 });
  }

  try {
    const upstream = await fetch(new URL("/chat", origin), {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ message }),
      signal: AbortSignal.timeout(280_000),
      cache: "no-store",
    });
    if (!upstream.ok) throw new Error(`Coach API returned ${upstream.status}`);
    const { reply } = await upstream.json();
    if (typeof reply !== "string" || !reply.trim()) throw new Error("Invalid coach reply");
    return Response.json({ reply }, { headers: { "Cache-Control": "no-store" } });
  } catch {
    return Response.json({ error: "The coach could not reply." }, { status: 502 });
  }
}
