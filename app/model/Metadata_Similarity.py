import pandas as pd
import requests
from bs4 import BeautifulSoup
import tldextract
from sklearn.metrics.pairwise import cosine_similarity
import csv
import re
import concurrent.futures
import spacy
from sentence_transformers import SentenceTransformer, util

# Load spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Load pre-trained transformer model for similarity checking
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

class TimeoutException(Exception):
    pass

class MetadataSimilarity:
    def __init__(self):
        pass

    def get_website_details(self, initial_url):
        try:
            response = requests.get(initial_url, allow_redirects=True)
            final_url = response.url
            html_content = response.text

            extracted_info = tldextract.extract(final_url)
            domain = f"{extracted_info.domain}.{extracted_info.suffix}"

            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            website_name = title_tag.string if title_tag else domain

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
        dataset = pd.read_csv(csv_file_path)
        print("Columns in the CSV:", dataset.columns)
        return dataset

    def clean_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        text = re.sub(r'\s+', ' ', text)
        return text

    def calculate_similarity(self, initial_url, csv_file_path):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.get_website_details, initial_url)
            try:
                extracted_features = future.result(timeout=30)
            except concurrent.futures.TimeoutError:
                print("Failed to extract features from the phishing website due to timeout.")
                return pd.DataFrame()

        if not extracted_features:
            print("Failed to extract features from the phishing website.")
            return pd.DataFrame()

        self.save_details_to_csv([extracted_features], 'phishing_website_details.csv')

        df = self.load_dataset(csv_file_path)

        website_names = df['website_name'].tolist()
        website_names.append(extracted_features['website_name'])
        name_embeddings = model.encode(website_names)
        name_similarities = cosine_similarity(name_embeddings[:-1], name_embeddings[-1].reshape(1, -1))

        urls = df['Original URL'].tolist()
        urls.append(extracted_features['phishing_url'])
        url_embeddings = model.encode(urls)
        url_similarities = cosine_similarity(url_embeddings[:-1], url_embeddings[-1].reshape(1, -1))

        combined_similarities = (name_similarities + url_similarities) / 2

        most_similar_index = combined_similarities.argmax()
        max_similarity = combined_similarities[most_similar_index]

        if max_similarity > 0.8:
            most_similar_website = df.iloc[most_similar_index]
            output_data = {
                'phishing_website_name': [extracted_features['website_name']],
                'phishing_url': [extracted_features['phishing_url']],
                'similar_website_name': [most_similar_website['website_name']],
                'similar_website_url': [most_similar_website['Original URL']],
                'similarity_score': [max_similarity]
            }
        else:
            output_data = {
                'phishing_website_name': [extracted_features['website_name']],
                'phishing_url': [extracted_features['phishing_url']],
                'similar_website_name': ['No similar website found'],
                'similar_website_url': ['No similar website found'],
                'similarity_score': [0]
            }

        output_df = pd.DataFrame(output_data)

        output_csv_path = 'similarity_results.csv'
        output_df.to_csv(output_csv_path, index=False)

        return output_df

if __name__ == "__main__":
    metadata_similarity_model = MetadataSimilarity()
    initial_url = "https://robiinhod-logim.gitbook.io/us"
    csv_file_path = "website_info.csv"
    result_df = metadata_similarity_model.calculate_similarity(initial_url, csv_file_path)
    print(result_df)
