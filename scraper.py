import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = "https://www.amazon.in/Apple-New-iPhone-12-128GB/dp/B08L5TNJHG/"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'lxml')

reviews = []
for review in soup.find_all('div', {'data-hook': 'review'}):
    title = review.find('a', {'data-hook': 'review-title'}).text.strip()
    text = review.find('span', {'data-hook': 'review-body'}).text.strip()

    style_tag = review.find('a', {'data-hook': 'format-strip'})
    style = style_tag.text.strip() if style_tag else 'N/A'

    color_tag = review.find('span', {'data-hook': 'review-color'})
    color = color_tag.text.strip() if color_tag else 'N/A'

    verified_purchase = 'Yes' if review.find('span', {'data-hook': 'avp-badge'}) else 'No'

    reviews.append({
        'Review Title': title,
        'Review Text': text,
        'Style': style,
        'Colour': color,
        'Verified Purchase': verified_purchase
    })

df = pd.DataFrame(reviews)
df.to_csv('iphone_reviews.csv', index=False)

engine = create_engine('sqlite:///reviews.db')
df.to_sql('reviews', con=engine, if_exists='replace', index=False)


engine = create_engine('sqlite:///reviews.db')
df = pd.read_sql('SELECT * FROM reviews', con=engine)
print(df)

