from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from urllib.parse import urlparse

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Website to scan (change this to your target website)
base_url = ""  # Change this to the target website
visited_urls = set()

def find_image(target_image_name, url):
    """Finds the specific image on the given page and returns its URL or the page it was found on."""
    print(f"Visiting: {url}")
    visited_urls.add(url)
    driver.get(url)
    time.sleep(2)  # Allow time for the page to load

    image_elements = driver.find_elements(By.TAG_NAME, "img")
    for img in image_elements:
        src = img.get_attribute("src")
        if src and os.path.basename(urlparse(src).path) == target_image_name:
            print(f"Image found: {src} on page {url}")
            return src, url

    # Extract links and crawl further
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith(base_url) and href not in visited_urls:
            result = find_image(target_image_name, href)
            if result:
                return result
    return None

# Define the target image name (e.g., "target_image.jpg")
target_image_name = "your__voice.jpg"  # Change this to the image you're looking for

# Start searching
result = find_image(target_image_name, base_url)
if result:
    print(f"Found image at: {result[0]} on page {result[1]}")
else:
    print("Image not found.")

# Close WebDriver
driver.quit()
