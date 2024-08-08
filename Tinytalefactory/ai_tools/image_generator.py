from .client_initializer import client


class ImageGenerator:

    def __init__(self):
        self.client = client
        self.model = 'dall-e-3'
        self.size = '1024x1024'
        self.quality = 'standard'
        self.n = 1
        self.images = ''
        self.prompt = ("Create vibrant, cartoon-like images for a children's book based on the paragraph I provide."
                       " The images should be bright, happy, and evoke positive feelings. DO NOT ADD ANY TEXT TO THE "
                       "image. ")

    def create_prompt(self, paragraph: str, appearance=''):
        """
        Override if you want to do custom validations or changes to the paragraph before generating an image.
        """
        self.prompt += f'The appearance of the kid is: {appearance}' if appearance != '' else ''

        self.prompt += f'The paragraph is: {paragraph}'

    def generate_image(self, paragraph: str, appearance=''):

        self.create_prompt(paragraph)

        response = self.client.images.generate(
            model=self.model,
            prompt=self.prompt,
            size=self.size,
            quality=self.quality,
            n=self.n,
        )

        image_url = response.data[0].url

        return image_url

