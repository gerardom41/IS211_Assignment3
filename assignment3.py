import csv
import argparse
import urllib.request
import re
from io import StringIO

image_regex = re.compile(r'\.(jpg|jpeg|gif|png)$', re.IGNORECASE)
fire_regex = re.compile(r'firefox', re.IGNORECASE)
chrome_regex = re.compile(r'chrome', re.IGNORECASE)
safari_regex = re.compile(r'version', re.IGNORECASE)
ie_regex = re.compile(r'trident', re.IGNORECASE)

def downloadData(url):
    """Downloads the data"""
    getData = urllib.request.urlopen(url)
    data = getData.read().decode('utf-8')

    return data 

def processData(data):
    data_file = StringIO(data)
    media = []
    browser = []
    
    read = csv.reader(data_file)
    for row in read:
        media.append(row[0])
        browser.append(row[2])
    
    return media, browser  

def searchImage(image_data):
    count, match = 0.0, 0.0

    for items in image_data:
        count += 1.0
        if image_regex.search(items):
            match += 1.0

    percentage = (match / count) * 100
    return percentage

def searchBrowser(browser_data):
    counts = {"Safari": 0, "Chrome": 0, "Fire": 0, "IE": 0}

    for items in browser_data:
        if safari_regex.search(items):
            counts["Safari"] += 1
        elif chrome_regex.search(items):
            counts["Chrome"] += 1
        elif fire_regex.search(items):
            counts["Fire"] += 1
        elif ie_regex.search(items):
            counts["IE"] += 1

    most_browser = max(counts, key=counts.get)
    return most_browser 

def main(url):
    print(f"Running main with URL = {url}...")

    data = downloadData(url)
    media, browser = processData(data)

    post_media = searchImage(media)
    print(f"Image requests account for {post_media}% of all requests")

    most_browser = searchBrowser(browser)
    print(f"{most_browser} is the most popular browser today")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

