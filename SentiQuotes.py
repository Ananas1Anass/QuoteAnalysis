import pandas as pd
from textblob import TextBlob
import plotly.graph_objects as go
import plotly.io as pio

df = pd.read_csv('quotes.csv')

unique_authors = df['author'].unique()

print("Available authors:")
for i, author in enumerate(unique_authors):
    print(f"{i+1}. {author}")

selected_author_indices = input("Enter author indices (comma-separated) or leave blank for all authors: ")
selected_author_indices = [int(idx.strip()) for idx in selected_author_indices.split(',')] if selected_author_indices else None
selected_authors = [unique_authors[idx-1] for idx in selected_author_indices] if selected_author_indices else None

min_text_length = int(input("Enter the minimum text length threshold: "))
max_text_length = int(input("Enter the maximum text length threshold: "))

filtered_quotes = df.copy()
if selected_authors:
    filtered_quotes = filtered_quotes[filtered_quotes['author'].isin(selected_authors)]
filtered_quotes = filtered_quotes[
    (filtered_quotes['text_length'] >= min_text_length) & (filtered_quotes['text_length'] <= max_text_length)
]

filtered_quotes['sentiment_polarity'] = filtered_quotes['text'].apply(lambda x: TextBlob(x).sentiment.polarity)

author_sentiment = filtered_quotes.groupby('author')['sentiment_polarity'].mean().reset_index()

author_sentiment = author_sentiment.sort_values('sentiment_polarity')

fig = go.Figure()
for author in author_sentiment['author']:
    data = author_sentiment[author_sentiment['author'] == author]
    fig.add_trace(go.Bar(x=data['author'], y=data['sentiment_polarity'], name=author))

fig.update_layout(
    title='Average Sentiment Polarity per Author',
    xaxis_title='Author',
    yaxis_title='Average Sentiment Polarity',
    xaxis_tickangle=-45
)

button_menu = []
button_menu.append(dict(label='All Authors', method='update', args=[{'visible': [True] * len(author_sentiment)}]))
for i, author in enumerate(author_sentiment['author']):
    visible = [False] * len(author_sentiment)
    visible[i] = True
    button_menu.append(dict(label=author, method='update', args=[{'visible': visible}]))

fig.update_layout(
    updatemenus=[
        dict(
            buttons=button_menu,
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            xanchor='left',
            yanchor='top'
        )
    ]
)

pio.show(fig)
