from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Setup WebDriver
service = Service(r"C:\drivers\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open Agoda website
driver.get("https://www.agoda.com/")

# Accept cookies if necessary
try:
    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="cookie-bar"]/div/div[2]/button'))
    )
    cookie_button.click()
except:
    print("No cookie banner found.")

# Close popups if they appear
try:
    close_popup = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'popup-close-button'))
    )
    close_popup.click()
    print("Popup closed successfully.")
except:
    print("No popup found.")

# Search for hotels in a destination
destination = "Paris"
search_box = driver.find_element(By.XPATH, '//*[@data-selenium="textInput"]')
search_box.send_keys(destination)
time.sleep(2)

# Scroll to search button to make sure it's visible
search_button = driver.find_element(By.XPATH, '//*[@data-selenium="searchButton"]')
driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
time.sleep(1)

# Wait for search button to be clickable and click using JavaScript
search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@data-selenium="searchButton"]'))
)
driver.execute_script("arguments[0].click();", search_button)  # Using JavaScript click

print("Search button clicked successfully.")

# Wait for search results to load
time.sleep(5)

# Scroll to load more results
for _ in range(3):  # Adjust the range to load more results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Extract hotel data
#hotels = driver.find_elements(By.XPATH, './/*[@data-selenium=".hotel-list-container .AgodaHomesBanner, .hotel-list-container .FacebookBanner, .hotel-list-container .LoginBanner, .hotel-list-container .LoginPriceGuaranteeBanner, .hotel-list-container .NoCCBanner, .hotel-list-container .PropertyCardContainer, .hotel-list-container .PropertyCardItem, .hotel-list-container .RecommendedFiltersBanner, .hotel-list-container>.PriceBreaker, .hotel-list-container>.PropertyCardItem"]')
hotels = driver.find_elements(By.XPATH, './/*[@data-element-name="property-card-info"]')
data = []

for index, hotel in enumerate(hotels[:100]):  # Limit to 100 records

    try:
        name = hotel.find_element(By.XPATH, './/*[@data-selenium="hotel-name"]').text
        print(name)
        # Find the price span of the first hotel
        #price_element = hotel.find_element(By.XPATH, '(//div[@class="hotel-container"])[1]//span[3]')
        #price = price_element.text
        #print(price)
        rating = hotel.find_element(By.XPATH, '//*[@id="contentContainer"]/div[4]/ol[1]/li[2]/div/a/div/div[2]/div[3]/div/div[1]/div/div/p').text
        print(rating)
        address = hotel.find_element(By.XPATH, './/*[@data-selenium="area-city-text"]').text
        print(address)
        
        # Add data to list
        data.append([name,  address])  # Add price, rating, and address if needed

    except Exception as e:
        print(f"Error scraping hotel: {e}")

# Save to CSV file
#csv_file = "agoda_hotels.csv"
#with open(csv_file, "a", newline="", encoding="utf-8") as file:
 #   writer = csv.writer(file)
  #  writer.writerow(["Name",  "Address"])
# writer.writerows(data)

#print(f"Scraped {len(data)} records and saved to {csv_file}")

# Close browser
driver.quit()
