"""Extract .jpg attachments from a saved Gmail get_message RAW result (JSON with a base64url `raw` field)."""
import sys, json, base64, email, os

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
raw = d['raw']; raw += '=' * (-len(raw) % 4)
msg = email.message_from_bytes(base64.urlsafe_b64decode(raw))
for p in msg.walk():
    fn = p.get_filename()
    if fn and fn.lower().endswith('.jpg'):
        open(os.path.join(out, os.path.basename(fn)), 'wb').write(p.get_payload(decode=True))
        print(fn)
