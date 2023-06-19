import csv
import requests
from bs4 import BeautifulSoup

def scrape_quotes():
    more_links = True
    page = 1
    quotes = []
    while more_links:
        markup = requests.get(f'http://quotes.toscrape.com/page/{page}').text
        soup = BeautifulSoup(markup, 'html.parser')
        for item in soup.select('.quote'):
            quote = {}
            quote['text'] = item.select_one('.text').get_text()
            quote['author'] = item.select_one('.author').get_text()
            tags = item.select_one('.tags')
            quote['tags'] = [tag.get_text() for tag in tags.select('.tag')]
            quote['page'] = page  # Add the page number to the quote
            quotes.append(quote)

        next_link = soup.select_one('.next > a')

        print(f'Scraped page {page}')

        if next_link:
            page += 1
        else:
            more_links = False
    return quotes

quotes = scrape_quotes()

# Save quotes to a CSV file
filename = 'quotes.csv'
with open(filename, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['text', 'author', 'tags', 'page']  # Include 'page' in fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(quotes)

print(f"Quotes saved to {filename}.")
