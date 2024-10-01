import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tinytalefactory.settings')
django.setup()


from Tinytalefactory.generate_stories.models import Story, Token
from django.contrib.auth import get_user_model


# user_model = get_user_model()
# user = user_model.objects.last()


# story = Story.objects.last().delete()
# new_story = Story.objects.create(title='New Title-2', user=user, info={'paragraphs': ['p1', 'p2'], 'img_urls': ['url1', 'url2']})


# story = Story.objects.last()
# print(story.info)
# info = story.info
# print(type(info))
# print(info['img_urls'])
# print(info['paragraphs'])