from openai import OpenAI
from Tinytalefactory.ai_tools.text_generator import StoryGenerator


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
    return response, story_generator.tokens_used




