from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import base64
from api_calls import process_image_and_prompt
import os
from os import listdir
import pandas as pd
import os.path

screenshot_names = []
results = []

def take_screenshot(df, cam_url, chromedriver_path, iterations_count, screenshots_frequency):

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
        df.loc[len(df.index)] = [img_name, process_image_and_prompt(img_name)]
        data.to_csv("data_new.csv")
    
  finally:
      # Clean up and close the browser window
      driver.quit()
  return df


if __name__ == "__main__":
  chromedriver_path = './chromedriver-mac-arm64/chromedriver'
  cam_url = 'https://www.youtube.com/watch?v=Mez4F1iFxxM&ab_channel=CornellLabBirdCams'
  iterations_count = 5
  screenshots_frequency = 5
  if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

  screenshot_dir = 'screenshots'
  # screenshot_names = [os.path.join(screenshot_dir, img) for img in os.listdir(screenshot_dir)]
  # results = [process_image_and_prompt(img) for img in screenshot_names]


  DIR = "data_new.csv"
  if os.path.isfile(DIR):
      data = pd.read_csv(DIR)
      take_screenshot(data, cam_url, chromedriver_path, iterations_count, screenshots_frequency)  

      # df_new = pd.DataFrame({"screenshots" : screenshot_names, "bird_tf": results})
      # data = pd.concat([df, df_new])
  else:
      data = pd.DataFrame(columns=["screenshot_names", "bird_tf"])

  # for img in os.listdir(DIR):
  #     screenshot_names.append(img)
  #     results.append(process_image_and_prompt(f"./screenshots/{img}"))
  data.to_csv("data_new.csv")

  df = pd.read_csv("data_new.csv")

  df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

  df.to_csv("data.csv", index=False)
