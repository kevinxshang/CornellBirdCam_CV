from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

# Specify the path to Chromedriver
# Specify bird cam URL
# Specify iterations
# Specify screenshots frequency
# Adjust if necessary 
chromedriver_path = './chromedriver-mac-arm64/chromedriver'
cam_url = 'https://www.youtube.com/watch?v=1ZL6py8uo3w'
iterations_count = 2
screenshots_frequency = 5

# Specify Chrome Options for headless
options = webdriver.ChromeOptions()
# Headless mode
options.add_argument('--headless') 
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox') 
options.add_argument('--disable-dev-shm-usage')
 # Autoplay videos
options.add_argument('--autoplay-policy=no-user-gesture-required')

# Set up the Chrome service and initialize the Chrome driver
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=Service(executable_path=chromedriver_path), options=options)
driver.get(cam_url)

# Wait for the live video to load
time.sleep(5)

try:
    '''
    # Will use this only with GUI (not headless)

    # Attempt to play the video by simulating a spacebar press
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE) 
    time.sleep(2)
    
    # Attempt to go full screen by clicking the full screen button
    fullscreen_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-fullscreen-button')
    fullscreen_button.click()
    time.sleep(2)
    '''
    
    for _ in range(iterations_count):
        # Take and save with "shots_frequency" pause time
        timestamp = int(time.time())
        date_time_format = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        driver.save_screenshot(f'screenshot_{date_time_format}.png')
        time.sleep(screenshots_frequency)
finally:
    # Clean up and close the browser window
    driver.quit()
