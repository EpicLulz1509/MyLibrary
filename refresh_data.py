"""
Refresh all library data with a single command.
This script:
1. Updates books & ratings from Goodreads export
2. Processes Kindle clippings for quotes
3. Ensures quotes have correct author information
"""

import os
import sys
from convert_csv import process_goodreads_export
from clippings import parse_clippings, remove_sub_highlights
import json


def main():
    print("=" * 60)
    print("REFRESHING LIBRARY DATA")
    print("=" * 60)

    updates = []
    errors = []

    # Step 1: Update books and ratings from Goodreads
    print("\n[1/2] Checking for Goodreads export...")
    goodreads_csv = 'goodreads_library_export.csv'

    if os.path.exists(goodreads_csv):
        print(f"Found {goodreads_csv}")
        try:
            books_data, reviews_data = process_goodreads_export(goodreads_csv)
            updates.append(f"Updated {len(books_data)} books")
            updates.append(f"Updated {len(reviews_data)} reviews")
        except Exception as e:
            errors.append(f"Failed to process Goodreads export: {e}")
    else:
        print(f"Warning: {goodreads_csv} not found - skipping Goodreads update")
        print("To update books/reviews:")
        print("  1. Go to https://www.goodreads.com/review/import")
        print("  2. Click 'Export Library' and download CSV")
        print("  3. Save as 'goodreads_library_export.csv' in this folder")

    # Step 2: Update quotes from Kindle clippings
    print("\n[2/2] Checking for Kindle clippings...")
    clippings_file = 'My Clippings.txt'

    if os.path.exists(clippings_file):
        print(f"Found {clippings_file}")
        try:
            # Load existing clippings if they exist
            existing_clippings = {}
            if os.path.exists('clippings.json'):
                try:
                    with open('clippings.json', 'r', encoding='utf-8') as f:
                        existing_clippings = json.load(f)
                    print(f"  Loaded existing clippings")
                except Exception as e:
                    print(f"  Warning: Could not load existing clippings: {e}")

            # Parse new clippings
            book_highlights = parse_clippings(clippings_file)
            filtered_highlights = remove_sub_highlights(book_highlights)

            # Merge with existing clippings (ADD new quotes, keep existing ones)
            new_quotes_count = 0
            for book, quotes in filtered_highlights.items():
                if book in existing_clippings:
                    # Add only new quotes that don't already exist
                    existing_quotes_set = set(existing_clippings[book])
                    new_quotes = [q for q in quotes if q not in existing_quotes_set]
                    existing_clippings[book].extend(new_quotes)
                    new_quotes_count += len(new_quotes)
                else:
                    # New book, add all quotes
                    existing_clippings[book] = quotes
                    new_quotes_count += len(quotes)

            # Save merged clippings
            with open('clippings.json', 'w', encoding='utf-8') as f:
                json.dump(existing_clippings, f, ensure_ascii=False, indent=4)

            total_quotes = sum(len(quotes) for quotes in existing_clippings.values())
            updates.append(f"Added {new_quotes_count} new quotes (total: {total_quotes} quotes from {len(existing_clippings)} books)")
        except Exception as e:
            errors.append(f"Failed to process Kindle clippings: {e}")
    else:
        print(f"Warning: {clippings_file} not found - skipping quotes update")
        print("To update quotes:")
        print("  1. Copy 'My Clippings.txt' from your Kindle to this folder")
        print("  2. Run this script again")

    # Print summary
    print("\n" + "=" * 60)
    print("REFRESH SUMMARY")
    print("=" * 60)

    if updates:
        print("\nSuccessfully updated:")
        for update in updates:
            print(f"  - {update}")

    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")

    if not updates and not errors:
        print("\nNo data files found to process.")
        print("Please add goodreads_library_export.csv or My Clippings.txt")

    print("\nNote: Quotes are automatically matched with authors from books.json")
    print("      using fuzzy matching when the server runs.")

    if updates and not errors:
        print("\nRestart your server to see the updated data:")
        print("  npm run dev:full")

    print("=" * 60)

    return 0 if not errors else 1


if __name__ == '__main__':
    sys.exit(main())
