import requests
from bs4 import BeautifulSoup
import tldextract
import csv
import time
import concurrent.futures
import pandas as pd

class PhishingDataExtraction:
    def __init__(self):
        pass

    def get_website_details(self, initial_url, timeout=30):
        try:
            # Fetch the website content with a timeout
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(requests.get, initial_url, allow_redirects=True)
                response = future.result(timeout=timeout)

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

        except (requests.RequestException, concurrent.futures.TimeoutError) as e:
            print(f"An error occurred: {e}")
            return None

    def save_details_to_csv(self, details_list, csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = details_list[0].keys() if details_list else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for details in details_list:
                writer.writerow(details)

    def extract_data(self, data):
        initial_urls = data.get('urls', [])
        timeout_seconds = data.get('timeout', 30)
        csv_file = 'website_details.csv'

        start_time = time.time()

        all_details = []
        for url in initial_urls:
            details = self.get_website_details(url, timeout_seconds)
            if details:
                all_details.append(details)

        end_time = time.time()

        # Save details to CSV
        self.save_details_to_csv(all_details, csv_file)
        print('Website details saved to:', csv_file)

        total_time = end_time - start_time
        print(f'Total time taken for extraction: {total_time:.2f} seconds')

        df = pd.read_csv(csv_file)
        print(df)
        return df

if __name__ == "__main__":
    initial_urls = [
        "https://robiinhod-logim.gitbook.io/us",
        "https://piscinaveronza.com/app/FTMLR/MTRLF/FRLDM/FRMLF",
        "https://pub-3e6b15201c5640728d997067a6de1de1.r2.dev/glogin.html",
        "http://oeuwkixlrqtcc.siydpvj.cn/",
        "http://www.bet365-654.com/",
        "https://amazon-store.itxcoins.com/",
        "https://arthur-matias.github.io/instagram-clone/",
        "http://fahrzeuge-mein.de/",
        "http://ws.bianjieshop.top/",
        "https://noticiasdasemana.com/inicio/",
        "http://www.snapchat-securisation.fr/",
        "http://pub-12861f6272e047cfb901babed2894e50.r2.dev/index3j.htm",
        "http://pub-b26443603be74865bdafa09363210cfe.r2.dev/load.htm",
        "http://pub-3247254dcb0a4f3b8d5e43a41e3015d2.r2.dev/eurxs.html",
        "http://khmerpornvideo.singup0.my.id/main.php",
        "http://www.yudian.tech/wordpress/indcx.html", 
        "http://www.mcar.cl/wp-content/upgrade/",
        "https://pub-ccf7597072154be388e6a3364c5b94a5.r2.dev/reward.html",
        "https://pub-ff85b3f6a2974a0e85ad06c43917a130.r2.dev/auth_start.html",
        "https://clientsbnbinfoaproving251001.com/65yadgdx",
        "http://netflix-omega-ebon.vercel.app/",
        "https://uncovered-fragrant-climb.glitch.me/public/eleventy.js.html",
        "https://sehawq.github.io/seeinstagrampost.github.io",
        "https://pqtb.pages.dev/",
        "https://bafybeic7egv4bneioj7yw5kf22rs7tg4khtfmtel7nrcitjfkntz7dqtvi.ipfs.infura-ipfs.io/",
        "https://midlajkari.github.io/NETFLIX-CLONE",
        "https://rapid-acidic-chronometer.glitch.me/",
        "https://ewqii.dsadrasdqw.club/",
        "http://ypxkyqvnhudbulzjvlpoz.kthkyiv.cn/",
        "https://homepage-coinbasepro.webflow.io/",
        "https://cien9.pages.dev/appeal_case_ID/",
        "https://mdtrnsvoi-vo.hubside.fr/",
        "https://votrorangsfixe.hubside.fr/",
        "https://beneficio-atualizar.pro/?flow=inputUsername",
        "http://midas.events-krafton.com/"
    ]
    extractor = PhishingDataExtraction()
    data = {'urls': initial_urls, 'timeout': 30}
    extractor.extract_data(data)
