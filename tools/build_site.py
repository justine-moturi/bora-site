"""Build a deployable static site from the working Bora page.

Usage: python3 -I build_site.py <src_files_dir> <out_dir>
"""
import os
import re
import shutil
import sys

src_dir, out_dir = sys.argv[1], sys.argv[2]
page = os.path.join(src_dir, "Bora — Microlending for Kenya's women's groups.html")
s = open(page, encoding="utf-8").read()

PREFIX = "./Bora — Microlending for Kenya's women's groups_files/"
LOVABLE = "https://id-preview--f8b74e0d-990a-4f5d-8d23-62c4c184cc7d.lovable.app/"


def cut(text, old, new="", count=1):
    n = text.count(old)
    assert n == count, f"expected {count} of {old[:80]!r}, found {n}"
    return text.replace(old, new)


# 1. Everything after </main> is Lovable badge, its scripts, and a browser-extension flyout.
i = s.index("</main>") + len("</main>")
s = s[:i] + "\n</body></html>\n"

# 2. Lovable badge styles in <head>.
s = re.sub(r"<style>\s*#lovable-badge.*?</style>", "", s, count=1, flags=re.S)

# 3. Lovable / preview scripts and preloads in <head>.
s = re.sub(r'<script defer="" src="[^"]*events\.[^"]*"[^>]*></script>', "", s, count=1)
s = re.sub(r'<link rel="modulepreload"[^>]*>', "", s)
s = cut(s, f'<link rel="icon" href="{LOVABLE}favicon.png" type="image/png">',
        '<link rel="icon" href="assets/bora_logo.png" type="image/png">')
assert "lovable.js" not in s and "index-D8ZG6fAO" not in s and "events.1248" not in s

# 4. In-page links that pointed at the old preview site.
s = re.sub(re.escape(LOVABLE) + r"\?__lovable_receipt=[^\"#]*(#[a-z]+)", r"\1", s)
assert LOVABLE not in s, "leftover preview link"

# 5. Contact form (no backend) -> Email us button.
form = re.search(r"<form\b.*?</form>", s, flags=re.S)
assert form
s = s[:form.start()] + (
    '<div class="mt-8"><a href="mailto:justinemoturi02@gmail.com?subject=Bora%20enquiry" '
    'class="inline-flex items-center justify-center whitespace-nowrap text-sm font-medium '
    'bg-primary text-primary-foreground shadow hover:bg-primary/90 h-10 px-8 rounded-full">'
    'Email us</a></div>'
) + s[form.end():]

s = re.sub(r"<!-- saved from url=.*?-->\n?", "", s, count=1)

# 6. Fix double-escaped apostrophes in twitter meta, drop dev-only attributes.
s = s.replace("&amp;#x27;", "&#x27;")
s = re.sub(r' data-tsd-source="[^"]*"', "", s)

# 7. Asset paths -> assets/.
s = s.replace(PREFIX + "css2", "assets/fonts.css")
s = s.replace(PREFIX, "assets/")
assert "_files/" not in s

# 8. Copy only the assets the page uses.
os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)
used = sorted(set(re.findall(r'assets/([^"\')\s]+)', s)))
for name in used:
    src_name = "css2" if name == "fonts.css" else name
    shutil.copy2(os.path.join(src_dir, src_name), os.path.join(out_dir, "assets", name))

open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(s)
print("index.html", len(s), "bytes")
print("assets:", ", ".join(used))
