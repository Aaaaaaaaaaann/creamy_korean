from googletrans import Translator
from django.utils.text import slugify


def translate_and_slugify(string):
    translator = Translator()
    translation = translator.translate(string, src='ru', dest='en')
    slug = slugify(translation.text.lower())
    return slug
