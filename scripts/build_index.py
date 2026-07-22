import os
import html

HTML_DIR = "."          # repo root
OUTPUT_PATH = "index.html"
SELF = "index.html"

files = sorted(
    f for f in os.listdir(HTML_DIR)
    if f.lower().endswith(".html") and f != SELF and os.path.isfile(f)
)

rows = "\n".join(
    f'      <li><a href="{html.escape(f)}">{html.escape(f)}</a></li>'
    for f in files
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Files</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <h1>Files</h1>
  <ul>
{rows}
  </ul>
</body>
</html>
"""

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(page)

print(f"Wrote {OUTPUT_PATH} listing {len(files)} file(s): {files}")
