from flask import Blueprint, request, jsonify , current_app

from app.model.HTML_Content_Similarity import HTMLContentSimilarity
from app.model.Legitimate_data_scrapping import LegitimateDataScraping
from app.model.Metadata_Similarity import MetadataSimilarity
from app.model.Phishing_data_extraction import PhishingDataExtraction
from app.model.phishing_detection_project1_url_based import PhishingDetection
from app.model.Website_Name_Similarity import WebsiteNameSimilarity
from app.model.openphish_scraper import OpenPhishScraper
bp = Blueprint('main', __name__)

html_similarity_model = HTMLContentSimilarity()
legitimate_data_scraping_model = LegitimateDataScraping()
metadata_similarity_model = MetadataSimilarity()
phishing_data_extraction_model = PhishingDataExtraction()
phishing_detection_model = PhishingDetection()
phishing_detection_model.load_model()  # Load the model
website_name_similarity_model = WebsiteNameSimilarity()

@bp.route('/html_similarity', methods=['POST'])
def html_similarity():
    data = request.json
    initial_url = data.get('initial_url')
    csv_file_path = data.get('csv_file_path')
    result = html_similarity_model.calculate_similarity(initial_url, csv_file_path)
    return jsonify(result.to_dict(orient='records'))

@bp.route('/legitimate_data_scraping', methods=['POST'])
def legitimate_data_scraping():
    data = request.json
    urls = data.get('urls')
    result = legitimate_data_scraping_model.scrape_data(urls)
    return jsonify(result)
    
@bp.route('/metadata_similarity', methods=['POST'])
def metadata_similarity():
    data = request.json
    initial_url = data.get('initial_url')
    csv_file_path = data.get('csv_file_path')
    result = metadata_similarity_model.calculate_similarity(initial_url, csv_file_path)
    return jsonify(result.to_dict(orient='records'))


@bp.route('/phishing_detection', methods=['POST'])
def phishing_detection():
    data = request.json
    if 'urls' not in data:
        return jsonify({"error": "Missing 'urls' key in request payload"}), 400
    
    urls = data['urls']
    if not isinstance(urls, list):
        return jsonify({"error": "'urls' should be a list"}), 400

    predictions = []
    for url in urls:
        try:
            predictions.append({
                "url": url,
                "is_phishing": bool(phishing_detection_model.predict([url])[0])
            })
        except Exception as e:
            predictions.append({
                "url": url,
                "error": str(e)
            })

    return jsonify(predictions), 200

@bp.route('/website_name_similarity', methods=['POST'])
def website_name_similarity():
    data = request.json
    initial_url = data.get('initial_url')
    csv_file_path = data.get('csv_file_path')
    result = website_name_similarity_model.calculate_similarity(initial_url, csv_file_path)
    if result is not None:
        return jsonify(result.to_dict(orient='records'))
    else:
        return jsonify({"error": "Failed to calculate similarity"}), 500

@bp.route('/run_scraper', methods=['GET'])
def run_scraper():
    scraper = OpenPhishScraper('https://openphish.com/feed.txt')
    scraper.run()
    return jsonify({"message": "Scraper ran successfully and data saved to phishing_urls.csv"}), 200

def run_scraper_job():
    with current_app.app_context():
        scraper = OpenPhishScraper('https://openphish.com/feed.txt')
        scraper.run()
        print("Scraper ran successfully and data saved to phishing_urls.csv")
