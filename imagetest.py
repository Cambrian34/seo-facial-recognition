from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
from urllib.parse import urljoin, urlparse
import hashlib


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
from urllib.parse import urljoin, urlparse

# Setup WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

# Initialize WebDriver
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    exit(1)

# Website to scan 
base_url = ""
# Set of visited URLs
visited_urls = set()
image_folder = "downloaded_images"

# Ensure image directory exists
os.makedirs(image_folder, exist_ok=True)
def download_image(image_url):
    """Download and save images locally with unique hash-based filenames"""
    try:
        # Send a GET request with a timeout of 5 seconds
        response = requests.get(image_url, stream=True, timeout=5)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Use the original filename from the URL
            filename = os.path.join(image_folder, os.path.basename(urlparse(image_url).path))

            # Save file
            with open(filename, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {image_url}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")


def extract_images():
    """Extracts and downloads images from the current page"""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
        image_elements = driver.find_elements(By.TAG_NAME, "img")
        image_urls = {img.get_attribute("src") for img in image_elements if img.get_attribute("src")}
        
        for url in image_urls:
            if url.startswith("http"):
                download_image(url)
    except Exception as e:
        print(f"Error extracting images: {e}")

def crawl_website(url):
    """Recursively crawls website and extracts images"""
    if url in visited_urls or not url.startswith(base_url):
        return

    print(f"Visiting: {url}")
    visited_urls.add(url)

    try:
        driver.get(url)
        time.sleep(2)  # Allow time for the page to load

        # Extract images from the current page
        extract_images()

        # Extract links and crawl further
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and href.startswith(base_url) and href not in visited_urls:
                crawl_website(href)

    except Exception as e:
        print(f"Error visiting {url}: {e}")

# Start crawling
crawl_website(base_url)

# Close WebDriver
driver.quit()