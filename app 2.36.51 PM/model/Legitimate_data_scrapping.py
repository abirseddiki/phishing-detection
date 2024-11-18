import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse

class LegitimateDataScraping:
    def __init__(self):
        pass

    def extract_website_info(self, website_url):
        # Send a GET request to the website URL
        try:
            response = requests.get(website_url)
            if response.status_code != 200:
                print(f"Failed to fetch {website_url}")
                return None, None, None, None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None, None, None, None
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract website name
        website_name = soup.find('title').text.strip() if soup.find('title') else None
        
        # Extract domain and original URL
        domain = urlparse(website_url).netloc
        original_url = website_url
        
        # Extract page source content
        page_source = str(soup)

        return website_name, domain, original_url, page_source

    def save_to_csv(self, data, filename):
        df = pd.DataFrame(data, columns=["website_name", "domain", "Original URL", "html_content"])
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def scrape_data(self, urls):
        all_data = []
        for website_url in urls:
            website_name, domain, original_url, page_source = self.extract_website_info(website_url)
            if website_name:
                data = {
                    "website_name": website_name,
                    "domain": domain,
                    "Original URL": original_url,
                    "html_content": page_source
                }
                all_data.append(data)
            else:
                print(f"Failed to extract information from {website_url}. Check the URL or try again later.")
        
        if all_data:
            self.save_to_csv(all_data, "website_info.csv")
        return all_data

# Example usage:
if __name__ == "__main__":
    urls = [
        "https://robinhood.com/",
        "https://piscinaveronza.com/",
        "https://mail.yahoo.com/",
        "https://www.google.co.uk/",
        "https://www.snapchat.com/",
        "https://www.dhl.com/",
        "https://www.payu.com/",
        "https://mail.google.com/",
        "https://www.sfr.fr/webmail",
        "https://www.chase.com/",
        "https://www.docusign.com/",
        "https://www.airbnb.com/",
        "https://www.netflix.com/",
        "https://www.navyfederal.org/",
        "https://www.yahoo.com/",
        "https://mail.google.com/",
        "https://www.netflix.com/",
        "https://mail.google.com/",
        "https://www.google.com/",
        "https://www.facebook.com/",
        "https://www.caixa.gov.br/",
        "https://robinhood.com/creditcard/", 
        "https://sherwood.news/", 
        "https://robinhood.com/", 
        "https://underthehoodpod.robinhood.com/", 
        "https://robinhood.com/us/en/about/legal/",  
        "https://applink.robinhood.com/security_privacy_settings", 
        "https://robinhood.com/us/en/about/options/", 
        "https://brokercheck.finra.org/", 
        "https://robinhood.com/us/en/about-us/", 
        "https://robinhood.com/support/", 
        "https://learn.robinhood.com", 
        "https://robinhood.com/l/privacy/", 
        "https://robinhood.com/us/en/our-commitments/",
        "https://robinhood.com/us/en/about/crypto/",  
        "https://careers.robinhood.com", 
        "https://robinhood.com/us/en/investor-index", 
        "https://robinhood.com/us/en/about/retirement/"
    ]
    scraper = LegitimateDataScraping()
    scraper.scrape_data(urls)
