import csv
import requests
from bs4 import BeautifulSoup

markup = requests.get('http://quotes.toscrape.com/').text

soup = BeautifulSoup(markup, 'html.parser')

quotes = []
for item in soup.select('.quote'):
    quote = {}
    quote['text'] = item.select_one('.text').get_text()
    quote['author'] = item.select_one('.author').get_text()
    tags = item.select_one('.tags')
    quote['tags'] = [tag.get_text() for tag in tags.select('.tag')]
    quotes.append(quote)

# Save quotes to a CSV file
filename = 'quotes.csv'
with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['text', 'author', 'tags'])
    writer.writeheader()
    writer.writerows(quotes)

print(f"Quotes saved to {filename}.")
