import os
from io import BytesIO

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tinytalefactory.settings')
django.setup()


from openai import OpenAI
from PIL import Image
import requests


class ImageVariation:

    def __init__(self):
        self.n = 5
        self.size = '1024x1024'
        self.client = OpenAI()

    def get_image(self):
        image_url = input('Image URL: ')
        response = requests.get(image_url)

        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image = image.convert('RGBA')
            image.save('downloaded_img.png', format='PNG')

        return

    def create_image_variation(self):

        with open('../downloaded_img.png', 'rb') as img_file:
            response = self.client.images.create_variation(
                image=img_file,
                n=self.n,
                size=self.size,
            )
            return response

    def start_image_variation(self):
        self.get_image()
        return self.create_image_variation()


image_variator = ImageVariation()
print(image_variator.start_image_variation())

# Very poor results.
