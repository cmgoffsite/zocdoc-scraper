import streamlit as st
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
                data = scrape_data(url)
                
                # Display scraped data
                st.write(data)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a valid URL")

if __name__ == "__main__":
    main()
