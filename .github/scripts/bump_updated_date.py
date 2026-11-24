#!/usr/bin/env python3
"""Refresh the "updated <date>" line in the hero pill of index.html (Hartmut, 24.11.2026:
"Write here updated November 25, 2026 and update this data every 2 days or so.").

Changes ONLY the date in the pill "● 17 offers live · German, French and English · updated <date>".
Before it writes, it checks that the pill's offer count equals the number of offer cards on the page;
if not, it stops with an error (no commit), because then the pill needs a real content update.

Usage: bump_updated_date.py [index.html] ["November 25, 2026"]   (no date = today in Europe/Berlin)
"""
import datetime, re, sys
from zoneinfo import ZoneInfo

path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
if len(sys.argv) > 2:
    new_date = sys.argv[2]
else:
    d = datetime.datetime.now(ZoneInfo("Europe/Berlin")).date()
    new_date = f"{d.strftime('%B')} {d.day}, {d.year}"

t = open(path, encoding="utf-8").read()
pat = re.compile(r'(<div class="flagpill">● <b>)(\d+)( offers live</b>[^<]*?updated )([^<]+)(</div>)')
hits = pat.findall(t)
if len(hits) != 1:
    sys.exit(f"STOP: expected one hero pill, found {len(hits)}")
pill_count = int(hits[0][1])
cards = len(re.findall(r'<article[^>]*class="card[ "]', t))
if cards != pill_count:
    sys.exit(f"STOP: pill says {pill_count} offers live, page has {cards} offer cards - needs a content update")
old_date = hits[0][3]
if old_date == new_date:
    print(f"no change: already 'updated {new_date}'")
    sys.exit(0)
t2 = pat.sub(lambda m: m.group(1) + m.group(2) + m.group(3) + new_date + m.group(5), t, count=1)
if t2.replace(new_date, old_date, 1) != t:
    sys.exit("STOP: something besides the date would change")
open(path, "w", encoding="utf-8").write(t2)
print(f"updated: '{old_date}' -> '{new_date}' ({cards} offers)")
