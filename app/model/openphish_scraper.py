# scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

class OpenPhishScraper:
    def __init__(self, url):
        self.url = url

    def fetch_html(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch page: {response.status_code}")

    def parse_html(self, html):
        urls = []

        # Assuming the phishing URLs are contained in a specific section or format
        for line in html.splitlines():
            if line.startswith('http'):
                urls.append(line.strip())
        return urls

    def save_to_csv(self, data, filename):
        df = pd.DataFrame(data, columns=['URL'])
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        print(f"Total URLs fetched: {len(data)}")
        print(f"Sample URLs: {data[:5]}")  # Print the first 5 URLs as a sample

    def run(self):
        html = self.fetch_html()
        urls = self.parse_html(html)
        self.save_to_csv(urls, 'phishing_urls.csv')
