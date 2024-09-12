from .client_initializer import client


class ImageGenerator:

    """Styles are vivid, or natural, vivid causes the images to be hyperreal"""

    def __init__(self):
        self.client = client
        self.model = 'dall-e-3'
        self.size = '1024x1024'
        self.quality = 'hd'
        self.n = 1
        self.images = ''
        self.prompt = ''
        self.style = 'vivid'

    def generate_image(self, prompt: str):

        self.prompt = prompt

        response = self.client.images.generate(
            model=self.model,
            prompt=self.prompt,
            size=self.size,
            quality=self.quality,
            n=self.n,
        )

        image_url = response.data[0].url

        return image_url

