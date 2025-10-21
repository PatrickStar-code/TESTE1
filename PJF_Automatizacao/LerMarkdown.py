import re
import json
from pathlib import Path

# === 1️ Load your markdown file ===
input_file = Path("output.md")
markdown_text = input_file.read_text(encoding="utf-8")

# === 2️ Split by each "Equipe :" block ===
team_blocks = re.split(r'\*\*Equipe\s*:\*\*', markdown_text)
teams = []

# === 3️ Parse each block individually ===
for block in team_blocks:
    if not block.strip():
        continue

    # Extract team info
    team_match = re.search(
        r'(\d+)\s*-\s*(.*?)\s*-\s*(.*?)\nINE\s*:\s*(\d+)\s*/\s*([^\n]+)',
        block, re.DOTALL
    )
    if not team_match:
        continue

    code, type_, name, ine, area = team_match.groups()

    

    # Extract members
    pattern = r'([A-ZÀ-Ú\s]+)\s+(\d+)\s*-\s*([A-ZÀ-Ú\s]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d/]+)'
    members = []

    if " - " in area:
        area = area.split(" - ", 1)[1].strip()

    for m in re.finditer(pattern, block):
        members.append({
            "name": m.group(1).strip(),
            "cbo": m.group(2),
            "role": m.group(3).strip(),
            "hours": int(m.group(4)),
            "microarea": int(m.group(5)),
            "other": int(m.group(6)),
            "start_date": m.group(7)
        })

    # Add to team list
    teams.append({
        "code": code,
        "name": f"{type_} - {name}",
        "ine": ine,
        "area": area.strip(),
        "members": members
    })

# === 4️⃣ Save all teams as JSON ===
output = {"teams": teams}
output_file = Path("teams_output.json")

with output_file.open("w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print(f"✅ {len(teams)} teams extracted and saved to {output_file.resolve()}")
