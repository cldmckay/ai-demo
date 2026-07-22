import os
import re
import html

REPO = os.environ["GITHUB_REPOSITORY"]          # e.g. "octocat/my-repo"
owner, repo_name = REPO.split("/")

# github.io pages base URL. If the repo IS "owner.github.io", pages serve at root.
if repo_name.lower() == f"{owner.lower()}.github.io":
    BASE_URL = f"https://{owner}.github.io/"
else:
    BASE_URL = f"https://{owner}.github.io/{repo_name}/"

README_PATH = "README.md"
OUTPUT_PATH = "index.html"

link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

def is_local_file_link(url: str) -> bool:
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return False
    return True

with open(README_PATH, encoding="utf-8") as f:
    readme_text = f.read()

entries = []
seen = set()
for text, target in link_pattern.findall(readme_text):
    target = target.split(" ")[0]  # strip any markdown title text
    if not is_local_file_link(target):
        continue
    local_path = target.lstrip("./")
    if not os.path.isfile(local_path):
        continue  # skip dead links so the index never 404s
    if target in seen:
        continue
    seen.add(target)
    entries.append((text, target))

rows = "\n".join(
    f'      <li><a href="{html.escape(BASE_URL + target)}">{html.escape(text)}</a></li>'
    for text, target in entries
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{html.escape(repo_name)} — Files</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <h1>{html.escape(repo_name)}</h1>
  <ul>
{rows}
  </ul>
</body>
</html>
"""

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(page)

print(f"Wrote {OUTPUT_PATH} with {len(entries)} link(s).")
