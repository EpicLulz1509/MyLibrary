import re
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
# output_path = "Grouped_Clippings.txt"

book_highlights = parse_clippings(input_path)
filtered_highlights = remove_sub_highlights(book_highlights)
# save_to_file(output_path, filtered_highlights)
# print(f"Grouped highlights saved to {output_path}")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_highlights, f, ensure_ascii=False, indent=4)
