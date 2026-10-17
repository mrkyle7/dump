"""Resize 112cam snapshots to 1440x1080 and burn in a timestamp caption bar.

Filenames look like 01_20261017141744048.jpg (camera local time, YYYYMMDDhhmmss + ms).
Writes 00.png, 01.png, ... in chronological order.
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
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle([0, 990, 1440, 1080], fill=(0, 0, 0, 160))
    d.text((40, 1012), label, font=font, fill='white')
    im.save(os.path.join(out, f"{i:02d}.png"))
    print(i, label)
