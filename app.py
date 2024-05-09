import streamlit as st
from scraper import scrape_data  # Import your scraper function
from selenium import webdriver

def main():
    st.title("ZocDoc Scraper")
    
    # User input for URL
    url = st.text_input("Enter the URL", "")
    
    # Button to start scraping
    if st.button("Scrape"):
        if url:
            try:
                # Specify the path to the ChromeDriver executable
                chrome_driver_path = "./chromedriver-mac-x64/chromedriver"
                
                # Create a Chrome WebDriver with the specified path
                driver = webdriver.Chrome(executable_path=chrome_driver_path)
                
                # Call the scraper function
                data = scrape_data(url, driver)
                
                # Display scraped data
                st.write(data)
                # Download the CSV file
                with open(csv_file_path, 'rb') as csvfile:
                    csv_data = csvfile.read()
                    b64 = base64.b64encode(csv_data).decode('utf-8')
                    href = f'<a href="data:file/csv;base64,{b64}" download="{csv_file_path}">Download CSV File</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    
                # Close the WebDriver
                driver.quit()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a valid URL")

if __name__ == "__main__":
    main()
