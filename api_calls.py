from screenshot_script import take_screenshot
import requests
import os
from os import listdir
import pandas as pd
import os.path
import base64

# Key here

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
    

if __name__ == "__main__":
  chromedriver_path = './chromedriver-mac-arm64/chromedriver'
  cam_url = 'https://www.youtube.com/watch?v=Mez4F1iFxxM&ab_channel=CornellLabBirdCams'
  iterations_count = 5
  screenshots_frequency = 5
  if not os.path.exists('screenshots'):
    os.makedirs('screenshots')
  take_screenshot(cam_url, chromedriver_path, iterations_count, screenshots_frequency)  

  screenshot_dir = 'screenshots'
  screenshot_names = [os.path.join(screenshot_dir, img) for img in os.listdir(screenshot_dir)]
  results = [process_image_and_prompt(img) for img in screenshot_names]


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

  df = pd.read_csv("data.csv")

  df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

  df.to_csv("data_new.csv", index=False)