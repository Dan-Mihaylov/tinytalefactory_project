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
        self.prompt = ("Create a disney style animated image based on the paragraph I provide. "
                       "If you are given the appearance of the person, you MUST ADHERE to it at all times, you will"
                       "be provided with the paragraph as well.")
        self.style = 'vivid'

    def create_prompt(self, paragraph: str, appearance=''):
        """
        Override if you want to do custom validations or changes to the paragraph before generating an image.
        """
        self.prompt += f'The appearance of the person is: {appearance}' if appearance != '' else ''

        self.prompt += f'The paragraph is: {paragraph}'

    def generate_image(self, paragraph: str, appearance=''):

        self.create_prompt(paragraph, appearance)

        response = self.client.images.generate(
            model=self.model,
            prompt=self.prompt,
            size=self.size,
            quality=self.quality,
            n=self.n,
        )

        image_url = response.data[0].url

        return image_url

