"""Build the standalone website (docs/index.html) from the game source.

index.html is the Artifact version: page content only, because claude.ai wraps it
in its own <head>. GitHub Pages needs a full page, so this adds the head that
claude.ai would normally provide, plus icons and link-preview tags.
Run:  python3 build.py
"""
from pathlib import Path

URL = 'https://lox-cafe.pages.dev/'
src = Path(__file__).with_name('index.html').read_text()

head = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="description" content="Run a cozy coffee shop: make drinks, warm pastries and keep customers happy. A Diner Dash-style game by Francheska Guerrero.">
<meta name="theme-color" content="#BFE6D5">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Lox Café">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta property="og:type" content="website">
<meta property="og:title" content="Lox Café">
<meta property="og:description" content="Run a cozy coffee shop: make drinks, warm pastries and keep customers happy.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{URL}preview.png">
<meta name="twitter:card" content="summary_large_image">
<style>
  :root {{ color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
  body {{ margin: 0; }}
  img {{ max-width: 100%; }}
  [hidden] {{ display: none !important; }}
</style>
<script>if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('sw.js'));</script>
'''
# The source starts with <title>/<link>/<style>, which belong in <head>; the
# markup starts at the game container.
split = src.index('<div class="game" id="game">')
page = head + src[:split] + '</head>\n<body>\n' + src[split:] + '\n</body>\n</html>\n'
out = Path(__file__).with_name('docs') / 'index.html'
out.write_text(page)
print('wrote', out, len(page), 'bytes')
# Offline support: stamp the service worker so each publish refreshes saved copies
import time
sw = Path(__file__).with_name('sw.template.js').read_text().replace('__VERSION__', time.strftime('%Y%m%d%H%M%S'))
(Path(__file__).with_name('docs') / 'sw.js').write_text(sw)
print('wrote docs/sw.js')
