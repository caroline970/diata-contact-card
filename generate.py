#!/usr/bin/env python3
"""
Diata Health digital contact card generator.

EDIT the CONTACT dict below, then run:  python3 generate.py
It rewrites two files in this folder:
  - index.html            (the pretty landing page you text people)
  - diata-health.vcf      (the actual contact file the "Save Contact" button serves)

This is the ONE place to edit. Change the Instagram handle here once and both the
page and the saved-contact card update on the next deploy.
"""

import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────────────
# EDIT YOUR DETAILS HERE  ← this is the single source of truth
# ─────────────────────────────────────────────────────────────────────────────
CONTACT = {
    "org":        "Diata Health",
    "tagline":    "Root-cause metabolic & weight care",
    "phone":      "(610) 520-1127",        # display format
    "phone_tel":  "+16105201127",          # dial format (no spaces)
    "email":      "hello@diatahealth.com",
    "website":    "https://diatahealth.com",
    "instagram":  "diatahealth",           # ← change handle here, everything updates
    "addr_street":"735 Old Lancaster Road",
    "addr_city":  "Bryn Mawr",
    "addr_state": "PA",
    "addr_zip":   "19010",
    "logo_file":  "assets/logo-navy.png",  # navy logo → page header + saved-contact photo
}

NAVY = "#20307f"
ICON_BG = "#eef1fb"   # soft navy tint behind each icon
# ─────────────────────────────────────────────────────────────────────────────


def b64(path):
    with open(os.path.join(HERE, path), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def maps_url(c):
    q = f"{c['addr_street']} {c['addr_city']} {c['addr_state']} {c['addr_zip']}"
    return "https://maps.apple.com/?q=" + q.replace(" ", "+")


def build_vcard(c, logo_b64):
    """vCard 3.0 — best iOS + Android compatibility. CRLF line endings required."""
    addr = f";;{c['addr_street']};{c['addr_city']};{c['addr_state']};{c['addr_zip']};USA"
    # Fold the base64 photo into 74-char continuation lines per RFC 2426.
    photo_line = "PHOTO;ENCODING=b;TYPE=PNG:" + logo_b64
    folded = [photo_line[:74]] + [" " + photo_line[i:i + 73] for i in range(74, len(photo_line), 73)]
    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:;{c['org']};;;",
        f"FN:{c['org']}",
        f"ORG:{c['org']}",
        f"TEL;TYPE=WORK,VOICE:{c['phone_tel']}",
        f"EMAIL;TYPE=WORK,INTERNET:{c['email']}",
        f"ADR;TYPE=WORK:{addr}",
        f"URL;TYPE=WORK:{c['website']}",
        f"URL;TYPE=Instagram:https://www.instagram.com/{c['instagram']}",
        f"X-SOCIALPROFILE;TYPE=instagram:https://www.instagram.com/{c['instagram']}",
        f"NOTE:{c['tagline']}",
        *folded,
        "END:VCARD",
    ]
    return "\r\n".join(lines) + "\r\n"


ICONS = {
    "call":   '<path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.07 21 3 13.93 3 5c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>',
    "text":   '<path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM7 9h10v2H7V9zm6 5H7v-2h6v2zm4-6H7V6h10v2z"/>',
    "email":  '<path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>',
    "instagram": '<path d="M12 2.2c3.2 0 3.6 0 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s0 3.6-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.6 0-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.21 15.6 2.2 15.2 2.2 12s0-3.6.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.4 2.21 8.8 2.2 12 2.2zm0 1.8c-3.15 0-3.52.01-4.76.07-.9.04-1.39.19-1.71.32-.43.17-.74.37-1.06.69-.32.32-.52.63-.69 1.06-.13.32-.28.81-.32 1.71C3.21 8.48 3.2 8.85 3.2 12s.01 3.52.07 4.76c.04.9.19 1.39.32 1.71.17.43.37.74.69 1.06.32.32.63.52 1.06.69.32.13.81.28 1.71.32 1.24.06 1.61.07 4.76.07s3.52-.01 4.76-.07c.9-.04 1.39-.19 1.71-.32.43-.17.74-.37 1.06-.69.32-.32.52-.63.69-1.06.13-.32.28-.81.32-1.71.06-1.24.07-1.61.07-4.76s-.01-3.52-.07-4.76c-.04-.9-.19-1.39-.32-1.71a2.85 2.85 0 0 0-.69-1.06 2.85 2.85 0 0 0-1.06-.69c-.32-.13-.81-.28-1.71-.32C15.52 4.01 15.15 4 12 4zm0 3.06A4.94 4.94 0 1 1 7.06 12 4.94 4.94 0 0 1 12 7.06zm0 8.15A3.21 3.21 0 1 0 8.79 12 3.21 3.21 0 0 0 12 15.21zm6.29-8.35a1.15 1.15 0 1 1-1.15-1.15 1.15 1.15 0 0 1 1.15 1.15z"/>',
    "website":'<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93C7.05 19.44 4 16.08 4 12c0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41C19.92 5.77 22 8.65 22 12c0 2.08-.81 3.98-2.1 5.39z"/>',
    "location":'<path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/>',
}

CHEVRON = '<svg class="chev" viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>'


def build_html(c, logo_b64):
    ig_url = f"https://www.instagram.com/{c['instagram']}"
    rows = [
        ("call",      "Call",      f"tel:{c['phone_tel']}",   ""),
        ("text",      "Text",      f"sms:{c['phone_tel']}",   ""),
        ("email",     "Email",     f"mailto:{c['email']}",    ""),
        ("instagram", "Instagram", ig_url,                    "_blank"),
        ("website",   "Website",   c['website'],              "_blank"),
        ("location",  "Location",  maps_url(c),               "_blank"),
    ]
    row_html = "\n".join(
        f'''      <a class="row" href="{href}"{f' target="{tgt}" rel="noopener"' if tgt else ''}>
        <span class="ico"><svg viewBox="0 0 24 24">{ICONS[key]}</svg></span>
        <span class="label">{label}</span>{CHEVRON}
      </a>''' for key, label, href, tgt in rows
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{c['org']} — Save our contact</title>
<meta name="description" content="{c['tagline']}">
<meta property="og:title" content="{c['org']}">
<meta property="og:description" content="Tap to save our contact details">
<meta property="og:image" content="assets/logo-navy.png">
<link rel="apple-touch-icon" href="assets/logo-navy.png">
<style>
  :root {{ --navy:{NAVY}; --icobg:{ICON_BG}; }}
  * {{ box-sizing:border-box; -webkit-tap-highlight-color:transparent; }}
  body {{
    margin:0; min-height:100vh; min-height:100dvh;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    background:linear-gradient(180deg,#eef2fb 0%, #dfe7f7 100%);
    color:#16224f; display:flex; justify-content:center;
    padding:max(28px,env(safe-area-inset-top)) 18px max(28px,env(safe-area-inset-bottom));
  }}
  .card {{
    width:100%; max-width:420px; background:#fff; color:#16224f;
    border-radius:30px; overflow:hidden; align-self:center;
    box-shadow:0 30px 70px rgba(22,34,79,.22), 0 2px 6px rgba(22,34,79,.08);
  }}
  .hero {{ text-align:center; padding:44px 26px 26px; }}
  .hero img {{ width:210px; max-width:66%; height:auto; }}
  .hero .tag {{
    color:#6b78a8; font-size:14.5px; margin-top:16px; letter-spacing:.3px; font-weight:500;
  }}
  .rows {{ padding:6px 18px; }}
  a.row {{
    display:flex; align-items:center; gap:16px; padding:15px 8px;
    text-decoration:none; color:#16224f; border-bottom:1px solid #eef0f6;
    transition:background .12s;
  }}
  a.row:last-child {{ border-bottom:none; }}
  a.row:active {{ background:#f5f7fd; }}
  .ico {{
    flex:0 0 46px; height:46px; border-radius:50%; background:var(--icobg);
    display:flex; align-items:center; justify-content:center;
  }}
  .ico svg {{ width:23px; height:23px; fill:var(--navy); }}
  .label {{ flex:1; font-size:18px; font-weight:600; letter-spacing:.2px; }}
  .chev {{ width:18px; height:18px; fill:none; stroke:#c2c8da; stroke-width:2.4;
           stroke-linecap:round; stroke-linejoin:round; }}
  .save {{ padding:20px 22px 30px; }}
  .save a {{
    display:block; text-align:center; background:var(--navy); color:#fff;
    text-decoration:none; font-size:18px; font-weight:700; letter-spacing:.3px;
    padding:19px; border-radius:18px; box-shadow:0 10px 24px rgba(32,48,127,.30);
  }}
  .save a:active {{ transform:translateY(1px); }}
  .hint {{ text-align:center; color:#9aa1b8; font-size:12.5px; margin-top:14px; line-height:1.5; }}
</style>
</head>
<body>
  <main class="card">
    <div class="hero">
      <img src="assets/logo-navy.png" alt="{c['org']}">
      <div class="tag">{c['tagline']}</div>
    </div>

    <div class="rows">
{row_html}
    </div>

    <div class="save">
      <a href="diata-health.vcf">＋ Save to Contacts</a>
      <div class="hint">Adds {c['org']} to your phone — iPhone &amp; Android, no app needed.</div>
    </div>
  </main>
</body>
</html>
"""


def main():
    logo_b64 = b64(CONTACT["logo_file"])
    with open(os.path.join(HERE, "diata-health.vcf"), "w", newline="") as f:
        f.write(build_vcard(CONTACT, logo_b64))
    with open(os.path.join(HERE, "index.html"), "w") as f:
        f.write(build_html(CONTACT, logo_b64))
    print("Wrote index.html and diata-health.vcf")


if __name__ == "__main__":
    main()
