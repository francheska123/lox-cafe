"""Turn art/logo-1024.png into every icon the game uses.
Run after make_logo.py:  python3 art/make_icons.py"""
import base64, io, subprocess, tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
logo = Image.open(ROOT / 'art' / 'logo-1024.png').convert('RGBA')
docs = ROOT / 'docs'
BLUE = (98, 160, 232, 255)

# Browser tab + Android/manifest icons: the full rounded tile
logo.resize((192, 192), Image.LANCZOS).save(docs / 'icon-192.png')
logo.resize((512, 512), Image.LANCZOS).save(docs / 'icon-512.png')

# iPhone home screen: iOS rounds the corners itself, so fill edge to edge
tile = logo.crop((100, 100, 924, 924))
bg = Image.new('RGBA', tile.size, BLUE); bg.alpha_composite(tile)
bg.convert('RGB').resize((180, 180), Image.LANCZOS).save(docs / 'apple-touch-icon.png')

# Link preview card for texts and social apps (1200x630)
og = Image.new('RGBA', (1200, 630), (198, 222, 250, 255))
big = logo.resize((560, 560), Image.LANCZOS)
og.alpha_composite(big, (320, 35))
og.convert('RGB').save(docs / 'preview.png')

# Small logo embedded in the game's title screen (works on claude.ai too)
buf = io.BytesIO(); logo.resize((200, 200), Image.LANCZOS).save(buf, 'PNG', optimize=True)
(ROOT / 'art' / 'logo-200.b64').write_text(base64.b64encode(buf.getvalue()).decode())

# Desktop launcher icon
with tempfile.TemporaryDirectory() as tmp:
    iconset = Path(tmp) / 'Lox.iconset'; iconset.mkdir()
    for s in (16, 32, 128, 256, 512):
        logo.resize((s, s), Image.LANCZOS).save(iconset / f'icon_{s}x{s}.png')
        logo.resize((s * 2, s * 2), Image.LANCZOS).save(iconset / f'icon_{s}x{s}@2x.png')
    app_icon = Path.home() / 'Desktop' / 'Lox Café.app' / 'Contents' / 'Resources' / 'AppIcon.icns'
    subprocess.run(['iconutil', '-c', 'icns', str(iconset), '-o', str(app_icon)], check=True)
print('icons updated')
