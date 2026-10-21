// Supabase Edge Function: openai-lead-event
//
// Proxies a "lead_created" conversion event to OpenAI's Ads events API.
// The real OpenAI API key lives only in this function's environment
// (set via `supabase secrets set OPENAI_EVENTS_API_KEY=...`), never in
// the website's HTML/JS or in git — the browser calls this function
// with no secret attached.

const OPENAI_EVENTS_URL =
  "https://bzr.openai.com/v1/events?pid=49rLrUkSxD88P1nYEShTpv";

const ALLOWED_ORIGINS = new Set([
  "https://airmedical24x7.com",
  "https://www.airmedical24x7.com",
]);

function corsHeaders(origin: string | null) {
  const allowOrigin = origin && ALLOWED_ORIGINS.has(origin) ? origin : "https://airmedical24x7.com";
  return {
    "Access-Control-Allow-Origin": allowOrigin,
    "Access-Control-Allow-Headers": "authorization, apikey, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
  };
}

Deno.serve(async (req) => {
  const origin = req.headers.get("origin");

  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders(origin) });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...corsHeaders(origin), "Content-Type": "application/json" },
    });
  }

  const apiKey = Deno.env.get("OPENAI_EVENTS_API_KEY");
  if (!apiKey) {
    return new Response(JSON.stringify({ error: "Server not configured" }), {
      status: 500,
      headers: { ...corsHeaders(origin), "Content-Type": "application/json" },
    });
  }

  let sourceUrl = "https://airmedical24x7.com/thank-you";
  try {
    const body = await req.json();
    if (typeof body?.source_url === "string" && body.source_url.length < 500) {
      sourceUrl = body.source_url;
    }
  } catch {
    // No/invalid body is fine; fall back to the default source_url above.
  }

  const eventId = crypto.randomUUID();

  const openaiRes = await fetch(OPENAI_EVENTS_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      validate_only: false,
      events: [
        {
          id: eventId,
          type: "lead_created",
          timestamp_ms: Date.now(),
          source_url: sourceUrl,
          action_source: "web",
          data: { type: "customer_action" },
        },
      ],
    }),
  });

  const ok = openaiRes.ok;
  return new Response(JSON.stringify({ ok, status: openaiRes.status }), {
    status: ok ? 200 : 502,
    headers: { ...corsHeaders(origin), "Content-Type": "application/json" },
  });
});
