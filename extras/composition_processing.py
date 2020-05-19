import re
import os
import logging
import sys
import django

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'creamy_korean.settings'
django.setup()

from django.core.exceptions import ObjectDoesNotExist

from products.models import Ingredient, Composition

logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ingredients.log'), filemode='a',
                    level=logging.WARNING, format='%(message)s')


def process_composition(instances):
    for composition in instances:
        ingrs_ids = []
        ingredients = composition.ingredients
        product = composition.product
        for ingr in ingredients:
            try:
                substance = Ingredient.objects.get(name__iexact=ingr)
            except ObjectDoesNotExist:
                try:
                    substance = Ingredient.objects.get(
                        name__iexact=re.sub(r'\s{2,}', ' ', (re.sub(r'\([0-9a-z-.,/+% ]+\)', '', ingr))).strip())
                except ObjectDoesNotExist:
                    logging.warning(f'Not matched: {ingr=}, {product.name=}')
                else:
                    ingrs_ids.append(substance.pk)
            else:
                ingrs_ids.append(substance.pk)
        if len(ingrs_ids) == len(ingredients):
            Composition.objects.update_or_create(product=product, defaults={'ingredients': ingrs_ids})
            composition.processed = True
            composition.save()
