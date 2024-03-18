from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import base64
import requests
import os
from os import listdir
import pandas as pd
import os.path

screenshot_names = []
results = []

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def process_image_and_prompt(input_image=None):

    # Path to your image
#     image_path = "path_to_your_image.jpg"

    # Getting the base64 string
    base64_image = encode_image(input_image)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Does this image contain a bird? Only respond with True or False."
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        json_response = response.json()
        content = json_response['choices'][0]['message']['content']
        return content
    else:
        return f"Error: {response.status_code} - {response.reason}"

# Specify the path to Chromedriver
# Specify bird cam URL
# Specify iterations
# Specify screenshots frequency
# Adjust if necessary 
chromedriver_path = './chromedriver-mac-arm64/chromedriver'
cam_url = 'https://www.youtube.com/watch?v=Mez4F1iFxxM&ab_channel=CornellLabBirdCams'
iterations_count = 5
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
        date_time_format = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        img_name = f'screenshots/screenshot_{date_time_format}.png'
        driver.save_screenshot(img_name)
        time.sleep(screenshots_frequency)
        screenshot_names.append(img_name)
        results.append(process_image_and_prompt(img_name))
    
finally:
    # Clean up and close the browser window
    driver.quit()

DIR = "data.csv"
if os.path.isfile(DIR):
    df = pd.read_csv(DIR)
    df_new = pd.DataFrame({"screenshots" : screenshot_names, "bird_tf": results})
    data = pd.concat([df, df_new])
else:
    data = pd.DataFrame({"screenshots" : screenshot_names, "bird_tf": results})

# for img in os.listdir(DIR):
#     screenshot_names.append(img)
#     results.append(process_image_and_prompt(f"./screenshots/{img}"))
data.to_csv("data.csv")