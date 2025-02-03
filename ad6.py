import csv
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # For sending key events
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# ------------------------------
# SETUP: Launch Chrome and initialize WebDriverWait
# ------------------------------
chromedriver_path = r"C:\Users\SPEED FORCE\OneDrive\Desktop\Nimish Project\chromedriver-win64\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 15)

# -----------------------------------------------
# Helper Function: select_date
# -----------------------------------------------
def select_date(date_value):
    """
    Attempts to click the calendar cell with a data-date attribute equal to date_value.
    It first checks the appropriate calendar header (using:
      - For March: /html/body/div[2]/div[4]/div[1]/table/thead/tr[1]/th[1]
      - For April: /html/body/div[2]/div[4]/div[1]/table/thead/tr[1]/th[2]
    If the desired month isn’t visible, it clicks the next-month button until it is,
    then clicks the desired date cell.
    """
    desired_date = datetime.datetime.strptime(date_value, "%Y-%m-%d")
    desired_month_name = desired_date.strftime("%B")  # e.g. "March" or "April"
    
    # Choose header xpath based on month.
    if desired_date.month == 3:
        header_xpath = "/html/body/div[2]/div[4]/div[1]/table/thead/tr[1]/th[1]"
    elif desired_date.month == 4:
        header_xpath = "/html/body/div[2]/div[4]/div[1]/table/thead/tr[1]/th[2]"
    else:
        header_xpath = "/html/body/div[2]/div[4]/div[1]/table/thead/tr[1]/th[2]"  # fallback

    date_xpath = f"//td[@data-date='{date_value}']"
    max_tries = 12
    for i in range(max_tries):
        try:
            header_text = driver.find_element(By.XPATH, header_xpath).text
            if desired_month_name not in header_text:
                # Click the next-month button until the desired month is visible.
                next_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'next')]")
                next_btn.click()
                time.sleep(1)
                continue
            # Once the desired month is visible, click the date cell.
            date_elem = wait.until(EC.element_to_be_clickable((By.XPATH, date_xpath)))
            date_elem.click()
            print(f"Selected date: {date_value}")
            return True
        except Exception as e:
            # In case the date cell isn’t clickable, try clicking the next-month button.
            try:
                next_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'next')]")
                next_btn.click()
                time.sleep(1)
            except Exception as ee:
                print("Error clicking next month button:", ee)
                break
    print(f"Could not select date {date_value}")
    return False

# -----------------------------------------------
# Main Code: Iterate over destinations and scrape results
# -----------------------------------------------
destinations = ["Copenhagen", "Rome", "Dubai", "Paris"]
all_flights = []

for dest in destinations:
    # Load the website fresh for each destination.
    driver.get("https://www.flightlist.io/")
    time.sleep(2)
    
    # --- Set Origin Field using keyboard simulation ---
    try:
        dep_input = wait.until(EC.element_to_be_clickable((By.ID, "from-input")))
        dep_input.clear()
        dep_input.send_keys("Frankfurt")
        time.sleep(2)  # Wait for suggestions to appear.
        dep_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        dep_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        print(f"[{dest}] Error setting origin: {e}")
    
    # --- Set Destination Field using keyboard simulation ---
    try:
        dest_input = wait.until(EC.element_to_be_clickable((By.ID, "to-input")))
        dest_input.clear()
        dest_input.send_keys(dest)
        time.sleep(2)
        dest_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        dest_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        print(f"[{dest}] Error setting destination: {e}")
    
    # --- Set Trip Type to "return" ---
    try:
        trip_type_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "type")))
        Select(trip_type_dropdown).select_by_value("return")
        time.sleep(1)
    except Exception as e:
        print(f"[{dest}] Error setting trip type: {e}")
    
    # --- Open the Date Picker ---
    try:
        date_picker = wait.until(EC.element_to_be_clickable((By.ID, "deprange")))
        date_picker.click()
        time.sleep(1)
    except Exception as e:
        print(f"[{dest}] Error opening date picker: {e}")
    
    # --- Clear Preselected Dates (if any) ---
    # Many date pickers mark the selected cell with a class such as "active".
    try:
        active_cells = driver.find_elements(By.XPATH, "//td[contains(@class, 'active')]")
        for cell in active_cells:
            # Click on the active cell to try to clear the selection.
            cell.click()
        time.sleep(1)
    except Exception as e:
        print(f"[{dest}] Error clearing preselected dates: {e}")
    
    # --- Select Departure Date Range: from March 15 to March 16, 2025 ---
    if not select_date("2025-03-15"):
        print(f"[{dest}] Failed to select departure start date.")
    time.sleep(1)
    if not select_date("2025-03-16"):
        print(f"[{dest}] Failed to select departure end date.")
    time.sleep(1)
    
    # --- Select Return Date Range: from April 1 to April 2, 2025 ---
    if not select_date("2025-04-01"):
        print(f"[{dest}] Failed to select return start date.")
    time.sleep(1)
    if not select_date("2025-04-02"):
        print(f"[{dest}] Failed to select return end date.")
    time.sleep(1)
    
    # --- Click the Apply button in the date picker ---
    try:
        apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'applyBtn')]")))
        apply_btn.click()
    except Exception as e:
        print(f"[{dest}] Error applying date selection: {e}")
    time.sleep(2)
    
    # --- Set Number of Passengers (2 adults) ---
    try:
        passengers_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "adults")))
        Select(passengers_dropdown).select_by_value("2")
        time.sleep(1)
    except Exception as e:
        print(f"[{dest}] Error setting passengers: {e}")
    
    # --- Submit the Search ---
    try:
        submit_btn = driver.find_element(By.ID, "submit")
        submit_btn.click()
    except Exception as e:
        print(f"[{dest}] Error clicking submit: {e}")
    time.sleep(7)
    
    # --- Scroll down to load additional results if needed ---
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    # --- Scrape Flight Results for the Current Destination ---
    try:
        flight_results = driver.find_elements(By.XPATH, "//*[@id='results']/ul/li")
        print(f"[{dest}] Found {len(flight_results)} flight(s).")
        
        for idx, flight in enumerate(flight_results, start=1):
            try:
                flight_price = flight.find_element(By.XPATH, "./div[1]/div[1]").text
                flight_departure = flight.find_element(By.XPATH, "./div[1]/div[2]/div[1]/div[2]/small").text
                flight_return = flight.find_element(By.XPATH, "./div[1]/div[2]/div[2]/div[3]/small").text
                route_from_origin = flight.find_element(By.XPATH, "./div[1]/div[2]/div[1]/div[3]/small").text
                route_from_destination = flight.find_element(By.XPATH, "./div[1]/div[2]/div[2]/div[4]/small").text
                
                all_flights.append([
                    dest, flight_price, flight_departure,
                    flight_return, route_from_origin, route_from_destination
                ])
                print(f"[{dest}] Scraped flight {idx}.")
            except Exception as e:
                print(f"[{dest}] Error scraping flight {idx}: {e}")
    except Exception as e:
        print(f"[{dest}] Error finding flight results: {e}")
    
    time.sleep(3)

# --- Save All Scraped Data to a CSV File ---
csv_file_path = os.path.join(os.path.dirname(__file__), "flights_destinations_merged.csv")
with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Destination", "Flight Price", "Departure", "Return Trip",
        "Route from Origin", "Route from Destination"
    ])
    writer.writerows(all_flights)

print(f"Scraping complete. Flight data saved to: {csv_file_path}")
driver.quit()
