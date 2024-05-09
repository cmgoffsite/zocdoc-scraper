from selenium import webdriver
from webdriver import webdriver_manager.chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from urllib.parse import urlparse

# Create a Chrome driver service
service = webdriver.Chrome(ChromeDriverManager().install())

# Initialize Chrome WebDriver with the service
driver = webdriver.Chrome(service=service)

def scrape_zocdoc_data(driver):
    # Find elements with the specified class name
    elements = driver.find_elements(By.CLASS_NAME, 'sc-2gkh1u-3')

    # Extract information from the elements
    data = []
    for element in elements:
        text = element.text
        href = element.get_attribute('href')
        data.append({'Text': text, 'Href': href})

    return data

def save_to_csv(data, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Text', 'Href']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def parse_additional_urls(url):
    # Parse the base URL
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    # Get the path and remove the trailing slash
    path = parsed_url.path.rstrip('/')

    # Generate additional URLs
    additional_urls = [f"{base_url}{path}/{i}" for i in range(2, 1000)]

    return additional_urls

def scrape_data(url):
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    all_data = []

    # Parse out additional URLs
    urls_to_scrape = [url] + parse_additional_urls(url)

    # Scrape data from all URLs
    for url in urls_to_scrape:
        try:
            # Open the webpage
            driver.get(url)

            # Wait for the elements to be present on the page
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-2gkh1u-3')))

            data = scrape_zocdoc_data(driver)
            all_data.extend(data)
            print("Data scraped from:", url)
        except Exception as e:
            print(f"Failed to scrape data from {url}: {str(e)}")
            break

    # Close the browser
    driver.quit()

    # Save all data to a single CSV file
    parsed_url = urlparse(url)
    last_level = parsed_url.path.split('/')[-1]
    csv_file_path = f"zocdoc_data_{last_level}.csv"
    save_to_csv(all_data, csv_file_path)

    return all_data, csv_file_path
