import json

# Step 1: load the raw bible data and reshape it into dictionary form:
# { "Genesis": { "1": { "1": "In the beginning...", "2": "..." }, "2": {...} }, ... }
with open("en_kjv.json", "r", encoding="utf-8-sig") as f:
    raw = f.read().strip()

# The file currently stores JS ("const bible = [...];") rather than pure JSON, so unwrap it.
if raw.startswith("const bible"):
    raw = raw[len("const bible ="):].strip().rstrip(";")

books = json.loads(raw)

bible = {}
for book in books:
    chapters = {}
    for chapter_index, verses in enumerate(book["chapters"], start=1):
        chapters[str(chapter_index)] = {
            str(verse_index): text
            for verse_index, text in enumerate(verses, start=1)
        }
    bible[book["name"]] = chapters

# Save the dictionary form as JSON.
with open("bible.json", "w", encoding="utf-8") as f:
    json.dump(bible, f, ensure_ascii=False, indent=2)

# Step 2: convert the dictionary form into a JS file.
with open("en_kjv.js", "w", encoding="utf-8") as f:
    f.write("const bible = ")
    json.dump(bible, f, ensure_ascii=False)
    f.write(";\n")
