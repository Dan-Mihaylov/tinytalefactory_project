from .client_initializer import client


class ImagePromptGenerator:

    def __init__(self):
        self.client = client
        self.model = 'gpt-4o'
        self.prompt = [
            {
                'role': 'system',
                'content': 'Act as a Dall-E-3 prompt generator, you might be provided with the appearance of the person'
                           ' the style of the image and a paragraph, you need to rewrite in order to describe the image'
                           ' accordingly. PLEASE RESPOND ONLY WITH THE PROMPT, NOTHING ELSE.'
            }
        ]
        self.tokens_user = 0

    def generate_prompt_from_info(self, image_style: str, appearance: str, paragraph: str):
        resulting_prompt = (
            f'The image style is {image_style}, the appearance of the person is: {appearance}, the '
            f'paragraph to describe is: {paragraph}.'
        )

        self.prompt.append({
            'role': 'user',
            'content': resulting_prompt
        })

        return self.prompt

    def assistant_response(self):
        response = self.client.chat.completions.create(
            model = self.model,
            messages= self.prompt
        )
        self.tokens_user += response.usage.total_tokens
        message_content = response.choices[0].message.content
        return message_content
