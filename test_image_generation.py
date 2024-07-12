import os
import django
from openai import OpenAI
from typing import List, Dict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tinytalefactory.settings')
django.setup()


client = OpenAI()


class ImageGeneration:

    def __init__(self, client: OpenAI):
        self.client = client
        self.model = "dall-e-3"
        self.size = "1024x1024"
        self.quality = "standard"
        self.prompt = ""
        self.n = 1
        self.tokens_used = 0
        self.images = ''

    def start_image_generation(self):

        print('---Image Generation---')
        query = input('What image do you like to generate?\n')
        self.prompt = query

        if self.prompt != '':
            return self.assistant_response()

        return self.quit()

    def assistant_response(self):
        print('Generating image... please wait..')

        response = self.client.images.generate(
            model=self.model,
            prompt=self.prompt,
            size=self.size,
            quality=self.quality,
            n=self.n,
        )

        image_url = response.data[0].url
        self.images += self.prompt + '\n' + image_url + '\n\n'

        print(image_url)

        if input('Continue Y/N: ').lower() == 'y':
            return self.continue_()

        return self.quit()

    def continue_(self):
        query = input('What image do you like to generate?\n')
        self.prompt = query

        if self.prompt != '':
            return self.assistant_response()

        return self.quit()

    def quit(self):
        answer = input('Save Image URLs? Y/N')

        if answer.lower() == 'y':
            file_name = input('File Name Without Extension: ')

            with open(f'prompt_results/{file_name}.txt', 'w') as file:
                file.write(self.images)
                file.write(f'Tokens Used: {self.tokens_used}')

            print('File Saved')

        print('Program Ended')


if __name__ == '__main__':
    image_generation = ImageGeneration(client)
    image_generation.start_image_generation()
