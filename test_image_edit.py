import os
import django
from openai import OpenAI
from typing import List, Dict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tinytalefactory.settings')
django.setup()


from openai import OpenAI


class ImageEditor:

    def __init__(self):
        self.client = OpenAI()
        self.image = ''
        self.prompt = ''
        self.model = 'dall-e-2'
        self.n = 1
        self.size  = '1024x1024'

    def get_image(self):
        image_url = input('Image URL: ')
        self.image = image_url
        return

    def get_prompt(self):
        prompt = input('Prompt: ')
        self.prompt = prompt
        return

    def get_response(self):
        response = self.client.images.edit(
            image=self.image,
            prompt=self.prompt,
            model=self.model,
            size=self.size,
            n=self.n
        )
        return response

    def start_edit(self):
        self.get_image()
        self.get_prompt()
        return self.get_response()


image_editor = ImageEditor()
print(image_editor.start_edit())

