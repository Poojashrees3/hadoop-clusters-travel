import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Selenium WebDriver
options =  webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without GUI
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
service = Service(r"C:\drivers\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)


# Open Hotels.com
driver.get("https://www.hotels.com/")
time.sleep(3)

# Accept Cookies
try:
    cookie_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_button.click()
except Exception:
    print("No cookie banner found.")
    
def close_pop_up(driver):
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Dismiss sign-in info."]'))  
        )
        close_button.click()
        print("popup closed") 
    except Exception as e:
        print("No popup found.")

# Search for hotels in a destination
destination = "Paris"
driver.find_element(By.CSS_SELECTOR, ".uitk-fake-input.uitk-form-field-trigger.uitk-field-fake-input.uitk-field-fake-input-hasicon").click()
driver.find_element(By.XPATH, './/*[@data-stid="destination_form_field-menu-input"]').send_keys(destination, Keys.ENTER)
driver.find_element(By.XPATH, './/*[@id="search_button"]').click()
time.sleep(5)
  # Wait for results
  
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.XPATH, './/*[contains(@class,"uitk-spacing uitk-spacing-margin-blockstart-two")]')))

# Scroll dynamically to load more hotels
for _ in range(15):  # Increase this to load more results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Find hotel cards (CORRECT XPATH)
hotel_cards = driver.find_elements(By.XPATH, './/*[contains(@class,"uitk-spacing uitk-spacing-margin-blockstart-two")]')

print(f"Total hotels found: {len(hotel_cards)}")

# Create directory for images


image_urls = set()  # Using a set to avoid duplicates

for index, hotel in enumerate(hotel_cards):
    try:
        # Find image in each hotel card (CORRECT TAG SELECTION)
        image_element = hotel.find_element(By.XPATH, './/img[contains(@class,"image")]')
        img_url = image_element.get_attribute("src")

        if img_url and "https" in img_url:
            image_urls.add(img_url)

        print(f"[{index+401}] Image found: {img_url}")

    except Exception:
        print(f"Could not find image for hotel {index+401}")

# Limit to 100 images
image_urls = list(image_urls)[:100]

# Download images
for idx, img_url in enumerate(image_urls):
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(f"new_hotels_images/hotel_{idx + 401}.jpg", "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        print(f"Downloaded {idx + 401}/{len(image_urls)}")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

# Close the browser
driver.quit()
print("✅ Image scraping complete!")
