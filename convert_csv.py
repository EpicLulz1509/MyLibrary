import csv
import json
import requests
import time
import re

def convert_rating(rating_str):
    """Convert Goodreads rating to our format"""
    if not rating_str or rating_str == '0':
        return 'Not rated'
    return f"{rating_str}/5"

def clean_title(title):
    """Clean up the title"""
    return title.strip()

def search_openlibrary(title, author, stats):
    """Search Open Library API for book and get cover"""
    try:
        # First attempt with original title
        query = f"{title} {author}".strip()
        url = f"https://openlibrary.org/search.json?q={requests.utils.quote(query)}&limit=1"

        print(f"    Searching Open Library API...")
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('docs') and len(data['docs']) > 0:
                book = data['docs'][0]

                # Try to get ISBN from search result
                if 'isbn' in book and book['isbn']:
                    isbn = book['isbn'][0]
                    cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
                    print(f"    Found ISBN via search: {isbn}")
                    stats['api_isbn'] += 1
                    return cover_url, 'api_isbn'

                # Try to get cover_i (cover ID)
                if 'cover_i' in book:
                    cover_id = book['cover_i']
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                    print(f"    Found cover ID via search: {cover_id}")
                    stats['api_cover_id'] += 1
                    return cover_url, 'api_cover_id'

        # If first search didn't help, remove parentheses and retry
        cleaned_title = re.sub(r'\([^)]*\)', '', title).strip()
        if cleaned_title and cleaned_title != title:  # Only retry if title actually changed
            print(f"    Retrying without parentheses: '{cleaned_title}'")
            query = f"{cleaned_title} {author}".strip()
            url = f"https://openlibrary.org/search.json?q={requests.utils.quote(query)}&limit=1"

            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get('docs') and len(data['docs']) > 0:
                    book = data['docs'][0]

                    # Try to get ISBN from search result
                    if 'isbn' in book and book['isbn']:
                        isbn = book['isbn'][0]
                        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
                        print(f"    Found ISBN via search (cleaned): {isbn}")
                        stats['api_isbn'] += 1
                        return cover_url, 'api_isbn'

                    # Try to get cover_i (cover ID)
                    if 'cover_i' in book:
                        cover_id = book['cover_i']
                        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                        print(f"    Found cover ID via search (cleaned): {cover_id}")
                        stats['api_cover_id'] += 1
                        return cover_url, 'api_cover_id'

        print(f"    Warning: No results from API search")
        stats['no_cover'] += 1
        return None, None

    except Exception as e:
        print(f"    Error: API search failed: {e}")
        stats['no_cover'] += 1
        return None, None

def get_book_cover(isbn13=None, isbn=None, title=None, author=None, stats=None):
    """Fetch book cover URL from Open Library with fallback"""
    if stats is None:
        stats = {}

    # Try ISBN13 first (most reliable)
    if isbn13:
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn13}-L.jpg"
        print(f"    Using ISBN13: {isbn13}")
        stats['direct_isbn'] += 1
        return cover_url, 'direct_isbn'

    # Fallback to ISBN if ISBN13 not available
    if isbn:
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        print(f"    Using ISBN: {isbn}")
        stats['direct_isbn'] += 1
        return cover_url, 'direct_isbn'

    # No ISBN - search Open Library API
    if title and author:
        print(f"    No ISBN, searching API...")
        return search_openlibrary(title, author, stats)

    print(f"    Warning: No ISBN or search data - placeholder will be shown")
    stats['no_cover'] += 1
    return None, None

def process_goodreads_export(csv_file='goodreads_library_export.csv'):
    """Convert Goodreads CSV export to our JSON formats"""

    books_data = []
    reviews_data = []

    # Statistics tracking
    stats = {
        'direct_isbn': 0,      # Covers from direct ISBN
        'api_isbn': 0,         # Covers from API search (found ISBN)
        'api_cover_id': 0,     # Covers from API search (cover ID)
        'no_cover': 0,         # No cover found
        'verified': 0          # Total covers found
    }

    print(f"Reading {csv_file}...")

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Only process books that have been read
            if row['Exclusive Shelf'] != 'read':
                continue

            # Extract book information
            title = clean_title(row['Title'])
            author = row['Author']

            # Extract both ISBN13 and ISBN separately
            isbn13 = None
            isbn = None

            if row.get('ISBN13') and row['ISBN13'].strip() and row['ISBN13'] != '=""':
                isbn13 = row['ISBN13'].strip('="').strip()

            if row.get('ISBN') and row['ISBN'].strip() and row['ISBN'] != '=""':
                isbn = row['ISBN'].strip('="').strip()

            book = {
                'title': title,
                'author': author,
                'cover_url': '',
                'url': f"https://www.goodreads.com/book/show/{row['Book Id']}",
                'avg_rating': row['Average Rating'],
                'user_rating': convert_rating(row['My Rating'])
            }

            # Get Open Library cover (try ISBN13, then ISBN, then API search)
            print(f"  [{len(books_data) + 1}] {title[:50]}...")
            cover_url, source = get_book_cover(isbn13=isbn13, isbn=isbn, title=title, author=author, stats=stats)
            book['cover_url'] = cover_url or ''

            # Verification already done in get_book_cover, so we can track it here
            if cover_url:
                stats['verified'] += 1

            # Small delay for API requests
            if not isbn13 and not isbn:  # Only delay when we made an API call
                time.sleep(0.5)

            books_data.append(book)

            # Extract review if it exists
            if row['My Review'] and row['My Review'].strip():
                review = {
                    'title': clean_title(row['Title']),
                    'author': row['Author'],
                    'cover_url': book['cover_url'],
                    'url': book['url'],
                    'rating': convert_rating(row['My Rating']),
                    'review': row['My Review'].strip(),
                    'date_read': row['Date Read'] if row['Date Read'] else None
                }
                reviews_data.append(review)

    # Save books data
    print(f"\nSaving {len(books_data)} books to books.json...")
    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(books_data, f, ensure_ascii=False, indent=4)

    # Save reviews data
    print(f"Saving {len(reviews_data)} reviews to reviews.json...")
    with open('reviews.json', 'w', encoding='utf-8') as f:
        json.dump(reviews_data, f, ensure_ascii=False, indent=4)

    print("\nConversion complete!")
    print(f"  - {len(books_data)} books saved to books.json")
    print(f"  - {len(reviews_data)} reviews saved to reviews.json")

    # Print cover statistics
    print(f"\n{'='*60}")
    print("COVER STATISTICS (Open Library)")
    print(f"{'='*60}")
    print(f"Direct ISBN covers:        {stats['direct_isbn']:3d} ({stats['direct_isbn']/len(books_data)*100:.1f}%)")
    print(f"API search (ISBN):         {stats['api_isbn']:3d} ({stats['api_isbn']/len(books_data)*100:.1f}%)")
    print(f"API search (Cover ID):     {stats['api_cover_id']:3d} ({stats['api_cover_id']/len(books_data)*100:.1f}%)")
    print(f"No cover found:            {stats['no_cover']:3d} ({stats['no_cover']/len(books_data)*100:.1f}%)")
    print(f"\nTotal covers found:        {stats['verified']:3d} ({stats['verified']/len(books_data)*100:.1f}%)")
    print(f"{'='*60}")

    # Print other stats
    rated_books = [b for b in books_data if b['user_rating'] != 'Not rated']
    print(f"\nOther Stats:")
    print(f"  - Books with ratings: {len(rated_books)}")
    print(f"  - Books with reviews: {len(reviews_data)}")

    return books_data, reviews_data

if __name__ == '__main__':
    try:
        process_goodreads_export()
    except FileNotFoundError:
        print("\nError: goodreads_library_export.csv not found!")
        print("\nPlease:")
        print("1. Go to https://www.goodreads.com/review/import")
        print("2. Click 'Export Library'")
        print("3. Download the CSV file")
        print("4. Save it as 'goodreads_library_export.csv' in this folder")
        print("5. Run this script again")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
