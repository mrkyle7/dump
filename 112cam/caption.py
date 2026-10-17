"""Resize 112cam snapshots to 1440x1080 and draw a matching timestamp caption bar.

Filenames look like 01_20261017141744048.jpg (camera local time, YYYYMMDDhhmmss + ms).
Writes 00.png, 01.png, ... (the snapshot) and 00_cap.png, ... (a transparent 1440x90 caption bar)
in chronological order. The bar is overlaid after the zoom in render.sh so it never gets cropped.
"""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
fonts = glob.glob('/usr/share/fonts/**/*Bold*.ttf', recursive=True) + glob.glob('/usr/share/fonts/**/*.ttf', recursive=True)
font = ImageFont.truetype(fonts[0], 44) if fonts else ImageFont.load_default()
for i, f in enumerate(sorted(x for x in os.listdir(src) if x.lower().endswith('.jpg'))):
    ts = f.split('_')[1]
    label = f"112cam  ·  {ts[6:8]}/{ts[4:6]}/{ts[0:4]}  {ts[8:10]}:{ts[10:12]}:{ts[12:14]}  ·  Person detected"
    im = Image.open(os.path.join(src, f)).convert('RGB').resize((1440, 1080), Image.LANCZOS)
    im.save(os.path.join(out, f"{i:02d}.png"))
    cap = Image.new('RGBA', (1440, 90), (0, 0, 0, 160))
    ImageDraw.Draw(cap).text((40, 22), label, font=font, fill='white')
    cap.save(os.path.join(out, f"{i:02d}_cap.png"))
    print(i, label)
