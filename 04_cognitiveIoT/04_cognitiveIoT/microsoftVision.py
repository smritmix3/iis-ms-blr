import sys
import os
import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

analyze_url = endpoint + "vision/v2.0/analyze"
analyze_url2 = endpoint + "vision/v2.0/detect"

# Set image_path to the local path of an image that you want to analyze.
# image_path = "D:\measure\Measuring_size_onA4-master\Measuring_size_onA4-master\img\\11.jpg"
image_path = "D:\measure\Measuring_size_onA4-master\Measuring_size_onA4-master\opencv\images\\5.jpg"

# image_path = "D:\measure\Measuring_size_onA4-master\Measuring_size_onA4-master\opencv\images\788.jpg"
# image_path ="D:\measure\Measuring_size_onA4-master\Measuring_size_onA4-master\788.jpg"
# image_path = "C:\Users\smrithi.fredric\Desktop\quality_person\quality person\788.jpg"
# image_path ="http://ec2-13-59-84-230.us-east-2.compute.amazonaws.com:8000/11.jpg"

# Read the image into a byte array
image_data = open(image_path, "rb").read()
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'}
params = {'visualFeatures': 'Categories,Description,Color'}
response = requests.post(
    analyze_url, headers=headers, params=params, data=image_data)
response_detect = requests.post(
    analyze_url2, headers=headers, params=params, data=image_data)
response.raise_for_status()
response_detect.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
detect = response_detect.json()
print(analysis)
image_caption = analysis["description"]["captions"][0]["text"].capitalize()
print(image_caption)

data = response_detect.json()
data = data.get("objects")[0]
#print(data["rectangle"]["w"])
width_in_pixel = data["rectangle"]["w"]
height_in_pixel = data["rectangle"]["h"]
object_detected = data["object"]
print("width: "+ str(width_in_pixel)+" height: "+ str(height_in_pixel)+ " object detected: "+object_detected)

# Display the image and overlay it with the caption.
image = Image.open(BytesIO(image_data))
plt.imshow(image)
plt.axis("off")
_ = plt.title(image_caption, size="x-large", y=-0.1)