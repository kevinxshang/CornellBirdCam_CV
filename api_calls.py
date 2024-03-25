# from screenshot_script import take_screenshot
import requests
import os
from os import listdir
import pandas as pd
import os.path
import base64

# key here

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