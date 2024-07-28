import pandas as pd
import requests
from bs4 import BeautifulSoup
import tldextract
from sklearn.metrics.pairwise import cosine_similarity
import csv
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from sentence_transformers import SentenceTransformer

# Load pre-trained transformer model for similarity checking
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

class WebsiteNameSimilarity:
    def __init__(self):
        pass

    def get_website_details(self, initial_url, timeout=30):
        try:
            # Setup requests retry strategy
            retry_strategy = Retry(
                total=3,  # Number of retries
                backoff_factor=1,  # A delay between retries
                status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP statuses
                method_whitelist=["HEAD", "GET", "OPTIONS"]  # Retry only on these HTTP methods
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            http = requests.Session()
            http.mount("http://", adapter)
            http.mount("https://", adapter)

            # Open the initial URL and handle redirects with timeout
            response = http.get(initial_url, timeout=timeout, allow_redirects=True)
            final_url = response.url
            html_content = response.text

            # Parse the final URL to extract the domain information
            extracted_info = tldextract.extract(final_url)
            domain = f"{extracted_info.domain}.{extracted_info.suffix}"

            # Parse the HTML content to extract the website name (if available)
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            website_name = title_tag.string if title_tag else domain

            # Store the details
            details = {
                'website_name': website_name,
                'phishing_url': initial_url,
                'phishing_redirect_url': final_url,
                'html_content': html_content
            }

            return details

        except (requests.RequestException) as e:
            print(f"An error occurred: {e}")
            return None

    def save_details_to_csv(self, details_list, csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = details_list[0].keys() if details_list else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for details in details_list:
                writer.writerow(details)

    def load_dataset(self, csv_file_path):
        # Load the dataset from a CSV file
        dataset = pd.read_csv(csv_file_path)
        print("Columns in the CSV:", dataset.columns)  # Print columns to verify
        return dataset

    def clean_html(self, html):
        # Remove HTML tags and extract meaningful text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        return text

    def calculate_similarity(self, initial_url, csv_file_path):
        # Extract features from the phishing website
        extracted_features = self.get_website_details(initial_url, timeout=30)
        if not extracted_features:
            print("Failed to extract features from the phishing website.")
            return None

        # Save the extracted phishing website details to CSV
        self.save_details_to_csv([extracted_features], 'phishing_website_details.csv')

        # Load the dataset
        df = self.load_dataset(csv_file_path)

        # Website name similarity
        website_names = df['website_name'].tolist()
        website_names.append(extracted_features['website_name'])
        name_embeddings = model.encode(website_names)
        name_similarities = cosine_similarity(name_embeddings[:-1], name_embeddings[-1].reshape(1, -1))

        # Find the most similar website
        most_similar_index = name_similarities.argmax()
        max_similarity = name_similarities[most_similar_index]

        # Prepare the output DataFrame
        if max_similarity > 0.8:  # Threshold for similarity
            most_similar_website = df.iloc[most_similar_index]
            output_data = {
                'phishing_website_name': [extracted_features['website_name']],
                'similar_website_name': [most_similar_website['website_name']],
                'similarity_score': [max_similarity]
            }
        else:
            output_data = {
                'phishing_website_name': [extracted_features['website_name']],
                'similar_website_name': ['No similar website found'],
                'similarity_score': [0]
            }

        output_df = pd.DataFrame(output_data)
        return output_df

if __name__ == "__main__":
    website_name_similarity_model = WebsiteNameSimilarity()
    initial_url = "https://robiinhod-logim.gitbook.io/us"
    csv_file_path = "website_info.csv"
    website_name_similarity_model.calculate_similarity(initial_url, csv_file_path)
