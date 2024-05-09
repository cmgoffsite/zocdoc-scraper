import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from urllib.parse import urlparse

def scrape_zocdoc_data(driver):
    elements = driver.find_elements(By.CLASS_NAME, 'sc-2gkh1u-3')
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
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    path = parsed_url.path.rstrip('/')
    additional_urls = [f"{base_url}{path}/{i}" for i in range(2, 1000)]
    return additional_urls

def main(url):
    driver = webdriver.Chrome()
    urls_to_scrape = [url] + parse_additional_urls(url)
    all_data = []
    for url in urls_to_scrape:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-2gkh1u-3')))
            data = scrape_zocdoc_data(driver)
            all_data.extend(data)
            st.write("Data scraped from:", url)
        except Exception as e:
            st.error(f"Failed to scrape data from {url}: {str(e)}")
            break
    driver.quit()
    parsed_url = urlparse(url)
    last_level = parsed_url.path.split('/')[-1]
    csv_file_path = f"zocdoc_data_{last_level}.csv"
    save_to_csv(all_data, csv_file_path)
    st.success("All data has been saved to:", csv_file_path)

if __name__ == "__main__":
    st.title("ZocDoc Web Scraper")
    url = st.text_input("Enter the initial URL:", "")
    if st.button("Scrape Data") and url:
        main(url)
