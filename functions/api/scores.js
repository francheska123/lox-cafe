// Lox Café shared arcade high scores (Cloudflare Pages Function + KV).
// GET  /api/scores?board=bar:3          -> top 10 for that board
// POST /api/scores {board, n, s}        -> adds the score if it makes the top 10
const BAD = new Set(['ASS', 'FUK', 'FUC', 'FCK', 'SHT', 'CUM', 'DIK', 'DIC', 'COK', 'KKK', 'NIG', 'NGR', 'FAG',
  'TIT', 'SEX', 'JIZ', 'VAG', 'PUS', 'FAP', 'KYS', 'NAZ', 'HOE', 'CNT', 'KNT', 'WTF', 'STF']);
const goodBoard = b => /^(bar|floor):\d{1,3}$/.test(b);
const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' };
const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...cors },
});

export const onRequestOptions = () => new Response(null, { headers: cors });

export async function onRequestGet({ request, env }) {
  const board = new URL(request.url).searchParams.get('board') || '';
  if (!goodBoard(board)) return json({ error: 'Unknown board.' }, 400);
  return json({ board, scores: (await env.SCORES.get(board, 'json')) || [] });
}

export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); } catch { return json({ error: 'Bad request.' }, 400); }
  const board = String(body.board || ''), n = String(body.n || '').toUpperCase(), s = Number(body.s);
  if (!goodBoard(board)) return json({ error: 'Unknown board.' }, 400);
  if (!/^[A-Z0-9]{3}$/.test(n)) return json({ error: 'Initials need 3 letters or numbers.' }, 400);
  if (BAD.has(n)) return json({ error: 'Pick different initials.' }, 400);
  const day = Number(board.split(':')[1]);
  // A loose sanity cap so obviously fake scores don't land on the board
  if (!Number.isFinite(s) || s <= 0 || s > 60 + day * 40) return json({ error: 'That score looks off.' }, 400);
  const list = (await env.SCORES.get(board, 'json')) || [];
  const entry = { n, s: Math.round(s * 100) / 100, t: Date.now() };
  list.push(entry);
  list.sort((a, b) => b.s - a.s);
  const top = list.slice(0, 10);
  const rank = top.indexOf(entry) + 1;
  if (rank) await env.SCORES.put(board, JSON.stringify(top)); // only write when it makes the board
  return json({ board, scores: top, rank });
}
