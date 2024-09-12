from openai import OpenAI
from Tinytalefactory.ai_tools.text_generator import StoryGenerator
from Tinytalefactory.ai_tools.image_generator import ImageGenerator

from cloudinary import uploader


SPLIT_BY = '|'
ASSET_FOLDER = 'ttf'


# TODO: if everything correct, must split the paragraphs on new line and then iterate through all items and generate img
# TODO: when images ready, pack everything in the JSON format for the database, with story title and all
def generate_story_from_questionary(name: str, story_about: str, special_emphasis: str, **kwargs):
    story_generator = StoryGenerator()
    story_generator.generate_prompt_from_questionary(
        name=name,
        story_about=story_about,
        special_emphasis=special_emphasis,
    )
    response = story_generator.assistant_response()
    story_text = format_text_to_paragraphs_in_list(response)
    return story_text, story_generator.tokens_used


def generate_story_from_category(category_name: str):
    """
    On index one of the list there will be the story title, because it is generated automatically from OpenAI
    when choosing to generate story from already pre-defined categories.
    """
    story_generator = StoryGenerator()
    story_generator.generate_prompt_from_category(category_name)
    response = story_generator.assistant_response()
    story_text = format_text_to_paragraphs_in_list(response)
    return story_text, story_generator.tokens_used


def generate_images_from_paragraphs(prompt: str):

    image_generator = ImageGenerator()

    image_url = image_generator.generate_image(prompt=prompt)

    return image_url


def format_text_to_paragraphs_in_list(text: str):
    paragraphs = text.split(SPLIT_BY)
    stripped_paragraphs = [p.strip() for p in paragraphs]
    filtered_paragraphs = list(filter(lambda x: x != '', stripped_paragraphs))
    return filtered_paragraphs

def gene():
    ...


# TODO: Maybe generate an asset folder based on the user?
def upload_image(image):
    response = uploader.upload(image, asset_folder=ASSET_FOLDER)
    if response:
        return response['secure_url']
