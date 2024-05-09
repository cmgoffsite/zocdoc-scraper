import streamlit as st
import base64
from scraper import scrape_data  # Import your scraper function

def main():
    st.title("ZocDoc Scraper")
    
    # User input for URL
    url = st.text_input("Enter the URL", "")
    
    # Button to start scraping
    if st.button("Scrape"):
        if url:
            try:
                # Call the scraper function
                data, csv_file_path = scrape_data(url)  # Modify your scraper function to return the CSV file path
                
                # Display scraped data
                st.write(data)
                
                # Download the CSV file
                with open(csv_file_path, 'rb') as csvfile:
                    csv_data = csvfile.read()
                    b64 = base64.b64encode(csv_data).decode('utf-8')
                    href = f'<a href="data:file/csv;base64,{b64}" download="{csv_file_path}">Download CSV File</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a valid URL")

if __name__ == "__main__":
    main()
