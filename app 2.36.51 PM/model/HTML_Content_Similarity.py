import pandas as pd
import requests
from bs4 import BeautifulSoup
import tldextract
from sklearn.metrics.pairwise import cosine_similarity
import csv
import re
import time
import spacy
from sentence_transformers import SentenceTransformer, util

# Load spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Load pre-trained transformer model for similarity checking
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

class HTMLContentSimilarity:
    def __init__(self):
        # Initialization code if needed
        pass

    def get_website_details(self, initial_url, timeout=30):
        try:
            # Open the initial URL and handle redirects with a timeout
            response = requests.get(initial_url, allow_redirects=True, timeout=timeout)
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

        except requests.RequestException as e:
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
            return

        # Save the extracted phishing website details to CSV
        self.save_details_to_csv([extracted_features], 'phishing_website_details.csv')

        # Load the dataset
        df = self.load_dataset(csv_file_path)

        # HTML content similarity
        html_contents = df['html_content'].apply(self.clean_html).tolist()
        html_contents.append(self.clean_html(extracted_features['html_content']))
        content_embeddings = model.encode(html_contents)
        content_similarities = cosine_similarity(content_embeddings[:-1], content_embeddings[-1].reshape(1, -1))

        # Find the most similar website
        combined_similarities = content_similarities.flatten()
        most_similar_index = combined_similarities.argmax()
        most_similar_website = df.iloc[most_similar_index]

        # Prepare the output DataFrame
        output_data = {
            'phishing_website_name': [extracted_features['website_name']],
            'phishing_url': [extracted_features['phishing_url']],
            'similar_website_name': [most_similar_website['website_name']],
            'similar_website_url': [most_similar_website['Original URL']],
            'similarity_score': [combined_similarities[most_similar_index]]
        }
        output_df = pd.DataFrame(output_data)

        # Save the output DataFrame to CSV
        output_csv_path = 'similarity_results.csv'
        output_df.to_csv(output_csv_path, index=False)

        # Print the output DataFrame
        print(output_df)
        return output_df

if __name__ == "__main__":
    html_similarity_model = HTMLContentSimilarity()
    initial_url = "https://robiinhod-logim.gitbook.io/us"
    csv_file_path = "website_info.csv"
    html_similarity_model.calculate_similarity(initial_url, csv_file_path)
