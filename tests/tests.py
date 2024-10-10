import os
import django
from openai import OpenAI
from typing import List, Dict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tinytalefactory.settings')
django.setup()

import cloudinary
from cloudinary import CloudinaryImage
from cloudinary import uploader, api
from django.contrib.auth import get_user_model

# IMAGE_URL = 'https://images.pexels.com/photos/26707538/pexels-photo-26707538/free-photo-of-gray-fox-in-the-snow.jpeg?auto=compress&cs=tinysrgb&w=350&h=250&dpr=1'
# response = uploader.upload(IMAGE_URL, asset_folder='ttf')
# print(response.secure_url)
# print(response)


user_model = get_user_model()

user = user_model.objects.first()
print(user.email)


# client = OpenAI()
#
#
# class Conversation:
#
#     def __init__(self, client: OpenAI):
#         self.client = client
#         self.messages = [
#             {
#                 'role': 'system',
#                 'content': 'You are a helpful assistant answering questions to the best of your ability.'
#             }
#         ]
#         self.tokens_used = 0
#
#     def start_conversation(self):
#
#         print('---Conversation---')
#         query = input('Ask your question:')
#         self.messages.append(
#             {'role': 'user', 'content': query}
#         )
#         return self.assistant_response()
#
#     def assistant_response(self):
#
#         response = self.client.chat.completions.create(
#             model='gpt-3.5-turbo',
#             messages=self.messages,
#         )
#         message_content = response.choices[0].message.content
#         self.messages.append(
#             {'role': 'system', 'content': message_content}
#         )
#         self.tokens_used += response.usage.total_tokens
#
#         print(f'Answer: {message_content}')
#         ask_new = input('Continue with questions? Y/N: ')
#
#         if ask_new.upper() == 'Y':
#             return self.continue_()
#
#         return self.quit()
#
#     def continue_(self):
#         query = input('New Question: ')
#
#         self.messages.append(
#             {'role': 'user', 'content': query}
#         )
#         return self.assistant_response()
#
#     def quit(self):
#         answer = input('Save Conversation? Y/N')
#
#         if answer.upper() == 'Y':
#             file_name = input('File Name Without Extension: ')
#
#             with open(f'{file_name}.txt', 'w') as file:
#                 messages_to_string = self.stringify(self.messages)
#                 file.write(messages_to_string)
#                 file.write(f'Tokens Used: {self.tokens_used}')
#
#             print('File Saved')
#
#         print('Program Ended')
#
#     @staticmethod
#     def stringify(messages: List[Dict]):
#         result = ''
#
#         for message in messages[1::]:
#             current = 'User: ' + message['content'] if message['role'] == 'user' else 'System: ' + message['content']
#             result += current + '\n'
#
#         return result
#
#
# if __name__ == '__main__':
#     conversation = Conversation(client)
#     conversation.start_conversation()


# class Categories:
#     KEYS = [
#         'adventure', 'fantasy', 'fairy_tales',
#         'animals', 'friendship', 'mystery',
#         'educational', 'family', 'humour', 'historical'
#     ]
#     ADVENTURE = 'Create an adventure story, filled with exciting journeys and quests.'
#     FANTASY = 'Create a fantasy story, magical worlds with mythical creatures and imaginative settings.'
#     FAIRY_TALES = 'Create a fairy tales story, classic tales with moral lessons and happy endings'
#     ANIMALS = 'Create an animals story, featuring animals as main characters, often with human like traits.'
#     FRIENDSHIP = 'Create a friendship story, book that explores the themes of friendship and relationships.'
#     MYSTERY = 'Create a mystery story, engaging story with puzzles and mysteries to solve.'
#     EDUCATIONAL = 'Create an educational story, book to teach concepts like numbers, letters and basic science'
#     FAMILY = 'Create a family story, that focuses on family dynamics and relationships.'
#     HUMOUR = 'Create a funny and entertaining story that makes children laugh.'
#     HISTORICAL = 'Create a historical story, that introduces kids to historical events and figures in an engaging way.'
#
#     @classmethod
#     def info(cls):
#         to_remove = [
#             '__module__', 'KEYS', 'info', '__dict__', '__weakref__', '__doc__', 'remove_keys', 'format_key_names'
#         ]
#         information = dict(cls.__dict__)
#         information = cls.remove_keys(to_remove, information)
#         information = cls.format_key_names(information)
#
#         print(information)
#
#     @staticmethod
#     def remove_keys(to_remove_keys_list: list, dictionary: dict):
#         [dictionary.pop(key) for key in to_remove_keys_list]
#         return dictionary
#
#     @staticmethod
#     def format_key_names(dictionary: dict):
#         return {
#             key.replace('_', ' ').lower().capitalize(): value
#             for key, value in dictionary.items()
#         }
#
#
# category = Categories()
# category.info()