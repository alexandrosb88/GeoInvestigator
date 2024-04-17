# GeoInvestigator

# Copyright (c) 2024 alexandrosb88

import cv2
import numpy as np
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import GeoScrapper


def load_screenshots(directory):

    print("\nRetrieving database...")
    
    screenshots = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img = cv2.imread(os.path.join(directory, filename))
            screenshots.append((filename, img))

    print("Database ready\n")
    
    return screenshots



def match_location(input_screenshot, saved_screenshots):

    print("\nSearching for matches...")
    
    
    matches = []
    match_score = 0

    for filename, saved_screenshot in saved_screenshots:

        result = cv2.matchTemplate(saved_screenshot, input_screenshot, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # uncomment to see the matching score for each image
        # print("filename " + filename + " has matching value " + str(max_val))
        
        match_score = max_val
        matches.append((filename, saved_screenshot, match_score))


    print("\nSearch complete! Find below the potential matches and see the relative images: \n")

    return matches


# Call Geoscapper to define the broad region and populate the database
north, south, east, west = GeoScrapper.define_region()
coordinates = GeoScrapper.generate_coordinates(north, south, east, west)
GeoScrapper.scrape_map(coordinates)


# Load the database
saved_screenshots_directory = input("Specify the path of the database folder: ")
saved_screenshots = load_screenshots(saved_screenshots_directory)


# Load the aerial image for analysis
image_path = input("Specify the path of your satelite image: ")
input_screenshot = cv2.imread(image_path)


# Matching
matches = match_location(input_screenshot, saved_screenshots)


# Sort the matches (higher first)
sorted_matches = sorted(matches, key=lambda x: x[2], reverse=True)


# Retrieve the top 5 potential matches
for i in range (5):
    filename, _ = os.path.splitext(sorted_matches[i][0])
    print ("Match no" + str(i + 1) + " Coordinates: " + filename + " -- Matching score: " + str(sorted_matches[i][2]))
    cv2.imshow("Match no" + str(i + 1) + " >> " + sorted_matches[i][0], sorted_matches[i][1])

cv2.waitKey(0)
cv2.destroyAllWindows()


# Ask for redirection
print("\n")

while True:

    try:
        user_selection = int(input("You can be redirected to the point of your choice by typing 1-5: "))
    
        if user_selection in [1, 2, 3, 4, 5]:
            break
        else:
            print("Invalid input.")
    except ValueError:
        print("Invalid input.")


    
selection_filename = sorted_matches[user_selection - 1][0]
lat = selection_filename[1:3]  + "." + selection_filename[3:8]
long = selection_filename[10:12]  + "." + selection_filename[12:17]

driver = webdriver.Chrome()
driver.get("https://www.google.com/maps/@" + lat + "," + long +",1400m/data=!3m1!1e3?entry=ttu")
time.sleep(5)

try:
        cookies = driver.find_element(By.XPATH, "//button[@jsname='tWT92d']")
        cookies.click()
        time.sleep(5)
except NoSuchElementException:
        pass





