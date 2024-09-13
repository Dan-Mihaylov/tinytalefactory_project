from .client_initializer import client


class ImagePromptGenerator:

    def __init__(self):
        self.client = client
        self.model = 'gpt-4o'
        self.prompt = [
            {
                'role': 'system',
                'content': 'Act as a Dall-E-3 prompt generator, Generate prompts for each paragraph, '
                           'if there are any characteristics for the main characters provided,'
                           'in the whole story, '
                           'make sure to include all of them in each prompt, and make sure they are detailed.'
                           'in order for the prompts to be more consistent, return the PROMPTS ONLY split by " | ".'
                           'Make sure there are only as many prompts as there are paragraphs.\n'
            }
        ]
        self.tokens_user = 0

    # def generate_prompt_from_info(self, image_style: str, appearance: str, paragraph: str):
    #     resulting_prompt = (
    #         f'The image style is {image_style}, the appearance of the person is: {appearance}, the '
    #         f'paragraph to describe is: {paragraph}.'
    #     )
    #
    #     self.prompt.append({
    #         'role': 'user',
    #         'content': resulting_prompt
    #     })
    #
    #     return self.prompt

    def generate_prompt_from_whole_story(self, story: str, image_style='', appearance=''):
        resulting_prompt = f'The whole story is: {story}'
        resulting_prompt += f'\n The image style is: {image_style}.' if image_style != '' else ''
        resulting_prompt += f'\n The appearance is: {appearance}.' if appearance != '' else ''

        self.prompt.append({
            'role': 'user',
            'content': resulting_prompt
        })

        return self.prompt

    def assistant_response(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.prompt
        )
        self.tokens_user += response.usage.total_tokens
        message_content = response.choices[0].message.content
        return message_content
