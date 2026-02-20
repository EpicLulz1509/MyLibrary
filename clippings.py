import re
import os
from collections import defaultdict
import json


def parse_clippings(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    clippings = content.split("==========")
    books = defaultdict(list)
    
    for clip in clippings:
        lines = clip.strip().split("\n")
        if len(lines) >= 3:
            title_line = lines[0].strip()
            book_title = title_line.split("(")[0].strip()  # Extract title before the parentheses
            highlight = lines[3].strip()
            # print(lines[3])
            if highlight:
                books[book_title].append(highlight)
    
    return books




def remove_sub_highlights(book_highlights):
    filtered_books = {}
    
    for book, highlights in book_highlights.items():
        sorted_highlights = sorted(highlights, key=len, reverse=True)
        filtered_highlights = []
        for highlight in sorted_highlights:
            if not any(highlight in larger for larger in filtered_highlights):
                filtered_highlights.append(highlight)
        filtered_books[book] = filtered_highlights
    
    return filtered_books




def save_to_file(output_path, books):
    with open(output_path, 'w', encoding='utf-8') as f:
        for book, highlights in books.items():
            f.write(f"{book}:\n")
            for h in highlights:
                f.write(f"  - {h}\n")
            f.write("\n")

    


input_path = "My Clippings.txt"
output_path = "clippings.json"

# Load existing clippings if they exist
existing_clippings = {}
if os.path.exists(output_path):
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            existing_clippings = json.load(f)
        print(f"Loaded existing clippings from {output_path}")
    except Exception as e:
        print(f"Warning: Could not load existing clippings: {e}")

# Parse new clippings
book_highlights = parse_clippings(input_path)
filtered_highlights = remove_sub_highlights(book_highlights)

# Merge with existing clippings (ADD new quotes, keep existing ones)
for book, quotes in filtered_highlights.items():
    if book in existing_clippings:
        # Add only new quotes that don't already exist
        existing_quotes_set = set(existing_clippings[book])
        new_quotes = [q for q in quotes if q not in existing_quotes_set]
        existing_clippings[book].extend(new_quotes)
        print(f"Added {len(new_quotes)} new quotes to '{book}'")
    else:
        # New book, add all quotes
        existing_clippings[book] = quotes
        print(f"Added new book '{book}' with {len(quotes)} quotes")

# Save merged clippings
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(existing_clippings, f, ensure_ascii=False, indent=4)

print(f"\nMerged clippings saved to {output_path}")
