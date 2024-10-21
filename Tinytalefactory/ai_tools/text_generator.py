from .client_initializer import client
# TODO: change count of paragraphs from 2 to 10


PARAGRAPHS_COUNT = 3

class StoryGenerator:

    def __init__(self):
        self.client = client
        self.model = 'gpt-4o'
        self.prompt = [
            {
                'role': 'system',
                'content': f'Act as a custom story books writer, where you will receive prompts from people, telling '
                           f'you more about the person and the persons hobbies or a story that they want to create a '
                           f'fond memory of, and you will be writing a {PARAGRAPHS_COUNT} VERY SHORT paragraphs '
                           f'NO MORE THAN 60 WORDS EACH of'
                           f' a story which includes the '
                           f'information you have been provided. MAKE SURE THERE ARE {PARAGRAPHS_COUNT} PARAGRAPHS.'
                           f' The paragraphs MUST BE SEPARATED BY A | symbol. '
                           f'Make sure the story is cheerful towards the person and catchy to read.'
            }
        ]
        self.tokens_used = 0

    def assistant_response(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.prompt
        )
        self.tokens_used += response.usage.total_tokens
        message_content = response.choices[0].message.content
        return message_content

    def generate_prompt_from_questionary(self, name: str, story_about: str, special_emphasis: str, **kwargs):
        resulting_prompt = (
            f'Generate a story about a person {f"the persons name is {name}" if name else ""} the story should be '
            f'detailed '
            f'and cheerful about {story_about}, {f"emphasise on {special_emphasis}" if special_emphasis else ""}'
        )

        self.prompt.append({
            'role': 'user',
            'content': resulting_prompt
        })
        return self.prompt

    def generate_prompt_from_category(self, category: str):

        create_title_prompt = (
            f' Start with the title of the story, just a plain text for the title, MAKE SURE title ends with'
            f' the separator " | ". Also make sure there are {PARAGRAPHS_COUNT} PARAGRAPHS in total.'
        )

        categories = {
            'adventure': Categories.ADVENTURE,
            'fantasy': Categories.FANTASY,
            'fairy_tales': Categories.FAIRY_TALES,
            'animals': Categories.ANIMALS,
            'friendship': Categories.FRIENDSHIP,
            'mystery': Categories.MYSTERY,
            'educational': Categories.EDUCATIONAL,
            'family': Categories.FAMILY,
            'humour': Categories.HUMOUR,
            'historical': Categories.HISTORICAL,
        }

        self.prompt.append({
            'role': 'user',
            'content': categories[category] + create_title_prompt
        })

        return self.prompt


class Categories:
    KEYS = [
        'adventure', 'fantasy', 'fairy_tales',
        'animals', 'friendship', 'mystery',
        'educational', 'family', 'humour', 'historical'
    ]
    ADVENTURE = f'Create an adventure story, filled with exciting journeys and quests.'
    FANTASY = f'Create a fantasy story, magical worlds with mythical creatures and imaginative settings.'
    FAIRY_TALES = f'Create a fairy tales story, classic tales with moral lessons and happy endings.'
    ANIMALS = f'Create an animals story, featuring animals as main characters, often with human like traits.'
    FRIENDSHIP = f'Create a friendship story, book that explores the themes of friendship and relationships.'
    MYSTERY = f'Create a mystery story, engaging story with puzzles and mysteries to solve.'
    EDUCATIONAL = f'Create an educational story, book to teach concepts like numbers, letters and basic science.'
    FAMILY = f'Create a family story, that focuses on family dynamics and relationships.'
    HUMOUR = f'Create a funny and entertaining story that makes children laugh.'
    HISTORICAL = f'Create a historical story, that introduces kids to historical events and figures in an engaging way.'

    @classmethod
    def info(cls):
        """
        Returns a dictionary with the Class Attributes as Keys and their values as values.
        Formats the result before returning with the helper staticmethod
        """

        to_remove = [
            '__module__', 'KEYS', 'info', '__dict__', '__weakref__', '__doc__', 'remove_keys', 'format_key_names'
        ]
        information = dict(cls.__dict__)
        information = cls.remove_keys(to_remove, information)
        information = cls.format_key_names(information)

        return information

    @staticmethod
    def remove_keys(to_remove_keys_list: list, dictionary: dict):
        [dictionary.pop(key) for key in to_remove_keys_list]
        return dictionary

    @staticmethod
    def format_key_names(dictionary: dict):
        return {
            key.replace('_', ' ').lower().capitalize(): value
            for key, value in dictionary.items()
        }
