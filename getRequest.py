mport requests
from bs4 import BeautifulSoup

markup = requests.get(f'http://quotes.toscrape.com/').text

soup = BeautifulSoup(markup, 'html.parser')

#all quotes
quotes = []

for item in soup.select('.quote'):
    quote = {}
    quote['text'] = item.select_one('.text').get_text()
    quote['author'] = item.select_one('.author').get_text()

    tags = item.select_one('.tags')

    quote['tags'] = [tag.get_text() for tag in tags.select('.tag')]
    quotes.append(quote)
    
print(quotes)