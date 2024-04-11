# GeoInvestigator

import cv2
import numpy as np
import os

def load_screenshots(directory):
    screenshots = []
    for filename in os.listdir(directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            img = cv2.imread(os.path.join(directory, filename))
            screenshots.append((filename, img))
    return screenshots



def match_location(input_screenshot, saved_screenshots):
    
    best_match = None
    best_match_score = float("-inf")

    for filename, saved_screenshot in saved_screenshots:

        result = cv2.matchTemplate(saved_screenshot, input_screenshot, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        print("filename " + filename + " has max value of " + str(max_val))

        if max_val > best_match_score:

            best_match_score = max_val
            best_match = saved_screenshot
            best_match_filename = filename

    return best_match, best_match_score, best_match_filename


saved_screenshots_directory = "saved_screenshots"
saved_screenshots = load_screenshots(saved_screenshots_directory)

input_screenshot = cv2.imread("test_1.png")

best_match, best_match_score, best_match_filename = match_location(input_screenshot, saved_screenshots)

print("Best Match is image: " + best_match_filename)

cv2.imshow("Best Match",best_match)
cv2.waitKey(0)
cv2.destroyAllWindows()
