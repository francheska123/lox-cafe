# Lox Café

A cozy Diner Dash-style coffee shop game by Francheska Guerrero.

Play it: https://lox-cafe.pages.dev/

- `index.html` is the game source (also published as a claude.ai Artifact).
- `docs/` is the website GitHub Pages serves. Rebuild it with `python3 build.py` after editing `index.html`.

- `functions/api/scores.js` is the shared high-score board (Cloudflare Pages Function + KV, see `wrangler.toml`).
- Publish with `./deploy.sh`.
