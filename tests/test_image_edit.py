import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tinytalefactory.settings')
django.setup()


from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageDraw


class ImageEditor:

    def __init__(self):
        self.client = OpenAI()
        self.image = None
        self.prompt = ''
        self.model = 'dall-e-2'
        self.n = 1
        self.size  = '1024x1024'

    def get_image(self):
        image_url = input('Image URL: ')
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image = image.convert('RGBA')
            image.save('downloaded_img.png', format='PNG')
            mask = Image.new('L', image.size, color=255)
            mask = mask.convert('RGBA')

            mask.save('mask_img.png', format='PNG')
        return

    def get_prompt(self):
        prompt = input('Prompt: ')
        self.prompt = prompt
        return

    def get_response(self):
        with open('../downloaded_img.png', 'rb') as img, open('../mask_img.png', 'rb') as mask:
            response = self.client.images.edit(
                image=img,
                prompt=self.prompt,
                model=self.model,
                size=self.size,
                n=self.n,
                mask=mask
            )
            return response

    def start_edit(self):
        self.get_image()
        self.get_prompt()
        return self.get_response()


image_editor = ImageEditor()
print(image_editor.start_edit())

