import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrape_kayak_prices(url):
    # Set the cookie parameters
    ck = {"name": "DATA_CONSENT", "value": 'false'}

    # Configure FirefoxOptions
    options = webdriver.FirefoxOptions()
    options.binary_location = '/Applications/Firefox.app'
    options.add_argument('--headless')  # Optional: Run in headless mode
    options.add_argument('--disable-gpu')  # Optional: Disable GPU acceleration

    # Set the executable_path within FirefoxOptions
    options.set_preference("webdriver.gecko.driver", '/path/to/geckodriver')

    # Create the Firefox WebDriver using the configured options
    driver = webdriver.Firefox(options=options)

    # Navigate to the URL
    driver.get(url)

    # Add the cookie
    driver.add_cookie(ck)

    # Wait for the page to load
    time.sleep(5)

    # Get the title of the page
    page_title = driver.title

    # Find price elements
    price_elements = driver.find_elements(By.CLASS_NAME, "f8F1-price-text")

    # Extract prices
    prices = []
    total_price = 0
    for price_element in price_elements:
        price_text = price_element.text
        # Remove any non-numeric characters from the price text
        price_numeric = int(''.join(filter(str.isdigit, price_text)))
        prices.append(price_numeric)
        total_price += price_numeric

    # Calculate the average
    average_price = total_price / len(prices) if prices else 0

    # Close the browser window
    driver.quit()

    return page_title, prices, average_price

# Streamlit app
st.title("Kayak Flight Price Scraper")
st.subheader("Instructions: Go to Kayak and enter your destination, dates and then search. Copy this search URL and paste it below to get the average price.")
# Get user input for the URL

url = st.text_input("Enter Kayak URL:", "https://www.kayak.it/flights/MIL-BOG/2024-03-01/2024-03-31")

if st.button("Get Average Price"):
    try:
        # Scrape data
        title, prices, average_price = scrape_kayak_prices(url)

        # Display results
        st.subheader("Flight Details:")
        st.write(title)

        st.subheader("Average Price:")
        st.write(f"{average_price:.2f}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
