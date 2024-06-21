import os
import django
from openai import OpenAI
from typing import List, Dict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tinytalefactory.settings')
django.setup()




client = OpenAI()


class Conversation:

    def __init__(self, client: OpenAI):
        self.client = client
        self.messages = [
            {
                'role': 'system',
                'content': 'You are a helpful assistant answering questions to the best of your anility.'
            }
        ]
        self.tokens_used = 0

    def start_conversation(self):

        print('---Conversation---')
        query = input('Ask your question:')
        self.messages.append(
            {'role': 'user', 'content': query}
        )
        return self.assistant_response()

    def assistant_response(self):

        response = self.client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=self.messages,
        )
        message_content = response.choices[0].message.content
        self.messages.append(
            {'role': 'system', 'content': message_content}
        )
        self.tokens_used += response.usage.total_tokens

        print(f'Answer: {message_content}')
        ask_new = input('Continue with questions? Y/N: ')

        if ask_new.upper() == 'Y':
            return self.continue_()

        return self.quit()

    def continue_(self):
        query = input('New Question: ')

        self.messages.append(
            {'role': 'user', 'content': query}
        )
        return self.assistant_response()

    def quit(self):
        answer = input('Save Conversation? Y/N')

        if answer.upper() == 'Y':
            file_name = input('File Name Without Extension: ')

            with open(f'{file_name}.txt', 'w') as file:
                messages_to_string = self.stringify(self.messages)
                file.write(messages_to_string)
                file.write(f'Tokens Used: {self.tokens_used}')

            print('File Saved')

        print('Program Ended')

    @staticmethod
    def stringify(messages: List[Dict]):
        result = ''

        for message in messages[1::]:
            current = 'User: ' + message['content'] if message['role'] == 'user' else 'System: ' + message['content']
            result += current + '\n'

        return result


if __name__ == '__main__':
    conversation = Conversation(client)
    conversation.start_conversation()
