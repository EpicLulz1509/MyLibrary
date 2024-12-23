import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.goodreads.com/review/list/33805951?shelf=read&page="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

books_data = []

def scrape_page(page_number):
    url = base_url + str(page_number)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    book_rows = soup.find_all("tr", {"class": "bookalike review"})
    if not book_rows:
        return False  
    
    for row in book_rows:
        book = {}
        cover = row.find("td", {"class": "field cover"})
        if cover:
            img_tag = cover.find("img")
            book["cover_url"] = img_tag["src"] if img_tag else None
            book["cover_url"] = book["cover_url"].replace('i.gr-assets.com', 'images-na.ssl-images-amazon.com')
            book["cover_url"] = book["cover_url"].replace('l/', 'i/')
            book["cover_url"] = book["cover_url"].replace(book["cover_url"][-11:-4], '')

            href_tag = cover.find("a")
            book["url"] = href_tag["href"] if href_tag else None
            book["url"] = "https://www.goodreads.com/" + book["url"]

        title = row.find("td", {"class": "field title"})
        book["title"] = title.get_text(strip=True) if title else None
        book["title"] = book["title"][5::]

        author = row.find("td", {"class": "field author"})
        book["author"] = author.get_text(strip=True) if author else None
        book["author"] = book["author"][6::]

        avg_rating = row.find("td", {"class": "field avg_rating"})
        book["avg_rating"] = avg_rating.get_text(strip=True) if avg_rating else None
        book["avg_rating"] = book["avg_rating"][10::]

        rating = row.find("td", {"class": "field rating"})
        book["user_rating"] = rating.get_text(strip=True) if rating else None
        book["user_rating"] = book["user_rating"][21::]
        if book["user_rating"] == "did not like it":
            book["user_rating"] = "1/5"
        elif book["user_rating"] == "it was ok":
            book["user_rating"] = "2/5"
        elif book["user_rating"] == "liked it":
            book["user_rating"] = "3/5"
        elif book["user_rating"] == "really liked it":
            book["user_rating"] = "4/5"
        elif book["user_rating"] == "it was amazing":
            book["user_rating"] = "5/5"

        books_data.append(book)
    
    return True

page = 1
while True:
    print(f"Scraping page {page}...")
    has_more_books = scrape_page(page)
    if not has_more_books:
        break
    page += 1

output_file = "books.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(books_data, file, ensure_ascii=False, indent=4)

print(f"Scraped data from {page - 1} pages saved to {output_file}")
