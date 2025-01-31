from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

def accepting_cookies(driver):
    #Accepting all cookies
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))  
        )
        cookie_button.click()
    except Exception as e:
        print("No cookie banner found.")
    return None

def close_pop_up(driver):
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Dismiss sign-in info."]'))  
        )
        close_button.click()
        print("popup closed") 
    except Exception as e:
        print("No popup found.")
    return None

def write_hotel_details(data):
    file_exists = os.path.exists("hotels.csv")
    with open("hotels.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["hotel_id", "hotel_name", "hotel_address", "hotel_city"])
        writer.writerows(data)
    return None

def write_review_details(data):
    file_exists = os.path.exists("reviews.csv")
    with open("reviews.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["review_id", "hotel_id", "rating", "review_description"])
        writer.writerows(data)
    return None

def write_image_details(data):
    file_exists = os.path.exists("images.csv")
    with open("images.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["image_id", "hotel_id", "image_path"])
        writer.writerows(data)
    return None

def write_price_details(data):
    file_exists = os.path.exists("prices.csv")
    with open("prices.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["price_id", "hotel_id", "room_type", "price_per_night","total_price"])
        writer.writerows(data) 
    return None