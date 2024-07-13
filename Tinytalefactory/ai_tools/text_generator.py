from openai import OpenAI
client = OpenAI()
# TODO: change count of paragraphs from 2 to 10


class StoryGenerator:

    def __init__(self, client: OpenAI):
        self.client = client
        self.model = 'gpt-3.5-turbo'
        self.prompt = [
            {
                'role': 'system',
                'content': 'Act as a custom children books writer, where you will receive prompts from people, telling '
                           'you more about their kid and the kids hobbies or a story that they want to create a fond '
                           'memory of, and you will be writing a 3 VERY SHORT paragraphs NO MORE THAN 60 WORDS EACH of'
                           ' a story which includes the '
                           'information you have been provided. The paragraphs MUST BE SEPARATED BY A \\n symbol. '
                           'Make sure the story is cheerful towards the kid and '
                           'catchy to read.'
            }
        ]
        self.tokens_used = 0

    def assistant_response(self):
        response = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=self.prompt
        )
        self.tokens_used += response.usage.total_tokens
        message_content = response.choices[0].message.content
        return message_content

    def generate_prompt_from_questionary(self, name: str, story_about: str, special_emphasis: str, **kwargs):
        resulting_prompt = (
            f'Generate a story about a kid {f"the kids name is {name}" if name else ""} the story should be detailed'
            f'and cheerful about {story_about}, {f"emphasise on {special_emphasis}" if special_emphasis else ""}'
        )

        self.prompt.append({
            'role': 'user',
            'content': resulting_prompt
        })
        return self.prompt

    def generate_generic_prompt(self):
        ...

