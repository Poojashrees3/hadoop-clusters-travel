from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from functions import accepting_cookies, close_pop_up, write_hotel_details, write_review_details, write_price_details, write_image_details
import requests

path = r"C:\Users\Varsha\OneDrive\Desktop\Binhvu\chromedriver-win64\chromedriver.exe"
service = Service(path)
# Set up Selenium WebDriver
driver = webdriver.Chrome(service=service)

# Open Booking.com
driver.get("https://www.booking.com")

#Accepting all cookies
accepting_cookies(driver)


#Closing popups
close_pop_up(driver)


# Search for hotels in a destination
destination = "Heidelberg" #Ran code in batches for each city
driver.find_element(By.CLASS_NAME, "eb46370fe1").send_keys(destination)

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Click the check-in field to open the calendar
checkin_field = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "a8887b152e")))
checkin_field.click()
time.sleep(5)

# Click next month arrow to load March month data
driver.find_element(By.CSS_SELECTOR, '[aria-label="Next month"]').click()

# Select the check-in date (e.g., "2025-02-15")
checkin_date = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="12 March 2025"]')))
checkin_date.click()
time.sleep(1)

# Select the check-in date (e.g., "2025-02-15")
checkout_date = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="31 March 2025"]')))
checkout_date.click()
time.sleep(1)

#Submit form to load results
driver.find_element(By.XPATH, '//*[contains(@class, "a83ed08757 c21c56c305 a4c1805887 f671049264 a2abacf76b c082d89982 cceeb8986b b9fd3c6b3c")]').click()

print("Reached scrolled page with results")
# Extract hotel data
time.sleep(5)

#Closing popups
close_pop_up(driver)

# Scroll to load more results
for _ in range(2):  
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)



hotels = driver.find_elements(By.XPATH, '//*[@data-testid="property-card"]')
data = []


for index,hotel in enumerate(hotels):
    try:
        name = hotel.find_element(By.XPATH, './/*[@data-testid="title"]').text
        total_price = hotel.find_element(By.XPATH, './/*[@data-testid="price-and-discounted-price"]').text[2:]
        rating = hotel.find_element(By.XPATH, './/*[@data-testid="review-score"]').text[7:10]
        price_per_night = round(int(total_price.replace(',', ''))/19,2)
        bed_type = hotel.find_element(By.XPATH, './/*[contains(@class,"abf093bdfe e8f7c070a7")]').text

        # Get image URL
        image_element = hotel.find_element(By.XPATH, './/*[@data-testid="image"]')
        image_url = image_element.get_attribute('src')
        print(name,total_price,rating,price_per_night,bed_type)

        # Download and save the image
        if image_url:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                image_path = f'booking-com/hotel_images/hotel_{index + 800}.jpg'
                with open(image_path, 'wb') as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
            else:
                image_path = "Image not available"
        else:
            image_path = "No image URL"

        write_image_details([(f'hotel_{index + 800}',f'hotel_{index + 800}',image_path)])


        # Getting more details
        # Extract hotel link
        hotel_link = hotel.find_element(By.XPATH, './/*[@data-testid="title-link"]').get_attribute("href")

        # Open the hotel's page in a new tab
        driver.execute_script("window.open(arguments[0]);", hotel_link)
        driver.switch_to.window(driver.window_handles[-1])
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the new page to load
        time.sleep(5)

        # Address
        address = driver.find_element(By.XPATH, './/*[contains(@class,"a53cbfa6de f17adf7576")]').text.split('\n')[0]

        # Review summary or a featured review
        try:
            review_summary = driver.find_element(By.XPATH, './/*[@data-testid="review-summary-desktop-summary"]').text
        except:
            try:
                review_summary = driver.find_element(By.XPATH, './/*[@data-testid="featuredreview-text"]').text
            except:
                review_summary = "Not Available"


        time.sleep(2)

        # Add details to data
        write_hotel_details([(f'hotel_{index + 800}',name, address,destination)])
        write_review_details([(f'review_{(2*index) + 800}',f'hotel_{index + 800}',rating,review_summary)])
        write_price_details([(f'hotel_{(3*index)+800}',f'hotel_{index + 800}',bed_type,price_per_night,int(total_price.replace(',', '')))])

        # Close the current tab and return to the main results page
        driver.close()
        time.sleep(1)
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)


    except Exception as e:
        print(f"Error: {e}")
    


print(len(data))


# Close the browser
driver.quit()
