from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import re
from functions import accepting_cookies, close_pop_up, write_hotel_details, write_review_details, write_price_details, write_image_details

# Set up Selenium WebDriver
service = Service(r"C:\drivers\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

options = webdriver.ChromeOptions()
options.add_argument("--lang=en")

# Open Hotels.com
driver = webdriver.Chrome(options=options)
driver.get("https://www.hotels.com/")
time.sleep(2)
# Accept cookies
accepting_cookies(driver)
# try:
#     cookie_button = WebDriverWait(driver, 5).until(
#         EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))  
#     )
#     cookie_button.click()
# except Exception as e:
#     print("No cookie banner found.")

# Close pop-ups
close_pop_up(driver)
# try:
#     close_button = WebDriverWait(driver, 5).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Dismiss sign-in info."]'))  
#     )
#     close_button.click()
#     print("popup closed") 
# except Exception as e:
#     print("No popup found.")

# Search for hotels in a destination
destination = "Paris, France"
driver.find_element(By.XPATH, './/*[@data-stid="destination_form_field-dialog-trigger"]').click()
driver.find_element(By.XPATH, './/*[@data-stid="destination_form_field-menu-input"]').send_keys(destination, Keys.ENTER)
driver.find_element(By.XPATH, './/*[@id="search_button"]').click()
time.sleep(5)

# Wait for results to load
#wait = WebDriverWait(driver, 60)


wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class,"uitk-spacing uitk-spacing-margin-blockstart-three")]')))

# Scroll to load more results
for _ in range(3):  # Adjust number of scrolls as needed
    driver.execute_script("window.scrollBy(0, 800);")  
    time.sleep(2)

# Get all hotel elements
hotels = driver.find_elements(By.XPATH, '//*[contains(@class,"uitk-spacing uitk-spacing-margin-blockstart-three")]')
print(f"Total hotels found: {len(hotels)}")
data = []

for index, hotel in enumerate(hotels):
    try:
        print(f"Processing hotel {index + 1}...")
        # Extract hotel name
       # try:
       #     name = hotel.find_element(By.XPATH, './/h3[contains(@class, "uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start")]').text
       #     print(name)
       # except Exception:                                               
       #     name = "No Name Found"
        #wait = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, './/*[contains(@class, "uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start")]')))
#
        #name = hotel.find_element(By.XPATH, './/h3[contains(@class, "uitk-heading uitk-heading-5 overflow-wrap uitk-layout-grid-item uitk-layout-grid-item-has-row-start")]').text
        #print(f"Total names found: {len(name)}")
        #print(name)
    #except Exception as e:
        #print(f"Skipping hotel due to missing name: {e}")
        #name = "No Name Found"
        
        #city = hotel.find_element(By.XPATH, './/div[contains(@class,"uitk-text uitk-text-spacing-half truncate-lines-2 uitk-type-300 uitk-text-default-theme")]').text
        #print(city)
       # try:
        #    price = hotel.find_element(By.XPATH, './/*[contains(@class, "uitk-layout-position uitk-layout-position-relative uitk-spacing uitk-spacing-padding-blockstart-half")]').text
        #    print(price)
        #except Exception:
        #    price = "No Price Found"                                                              
        #bed_type = "Double bed"
        #print(bed_type)
        #scrapped_rating = hotel.find_element(By.XPATH, './/*[contains(@class, "uitk-badge-base-text")]').text
        #rating =int(scrapped_rating.replace(',', ''))
        #print(rating)
        # Get image URL
     

        #write_image_details([(f'hotelimage_{index + 400}',f'hotel_{index + 400}',image_path)])
        # Getting more details
        # Extract hotel link
        hotel_link = hotel.find_element(By.XPATH, '//*[contains(@class,"uitk-card-link")]').get_attribute("href")
        
        # Open the hotel's page in a new tab
        driver.execute_script("window.open(arguments[0]);", hotel_link)
        driver.switch_to.window(driver.window_handles[-1])
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the new page to load
        time.sleep(5)
        try:
            #wait = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, './/img[contains(@class,"uitk-image-media")]')))
            image_element = hotel.find_element(By.XPATH, './/*[contains(@class,"uitk-image-media")]') 
            image_url = image_element.get_attribute('src') or image_element.get_attribute('data-src')  # Use 'src' or 'data-src' based on the website
            print(image_url)
            time.sleep(3)

        #print(name,price,rating,image_url)
        # Download and save the image
           # if image_url:
              #  response = requests.get(image_url, stream=True)
              #  if response.status_code == 200:
                 #   image_path = f'h_hotels_images/hotel_{index + 400}.jpg'
                  #  with open(image_path, 'wb') as img_file:
                     #   for chunk in response.iter_content(1024):
                          #  img_file.write(chunk)
           #     else:
               #     image_path = "Image not available"
           # else:
             #   image_path = "No image URL"
        except Exception:
            image_path = "No image URL"
            print(image_path)
        # Address
        scrapped_address = driver.find_element(By.XPATH, './/div[contains(@class,"uitk-text uitk-type-300 uitk-text-default-theme uitk-layout-flex-item uitk-layout-flex-item-flex-basis-full_width")]').text
        #text_address = scrapped_address
        address = scrapped_address.replace(',', ' ')
        print(address)
        #try:
        scrapped_summary = driver.find_element(By.XPATH, './/p[contains(@class,"uitk-paragraph uitk-paragraph-2")]').text
        review_summary = scrapped_summary.replace(',', ' ')
        #except:
            #try:
            #    review_summary = driver.find_element(By.XPATH, './/*[@data-testid="featuredreview-text"]').text
           # except:
            #review_summary = "Not Available"
        print(review_summary)
        # Store data
       # write_hotel_details([(f'hotel_{index + 400}',name, address,destination)])
        #write_review_details([(f'review_{(2*index) + 400}', f'hotel_{index + 400}' ,rating,review_summary)])
        #write_price_details([(f'price_{(3*index)+400}',f'hotel_{index + 400}',price)])

        # Close the current tab and return to the main results page
        # Close the current tab and return to the main results page
        driver.close()
        time.sleep(1)
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)


    except Exception as e:
        print(f"Error: {e}")
    

# # Save to CSV
# with open("hotels.csv", "w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Name", "Price", "Rating"])
#     writer.writerows(data)

print(data)
print(len(data))


# Close the browser
driver.quit()

