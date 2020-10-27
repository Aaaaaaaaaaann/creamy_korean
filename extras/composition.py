import re
import os
import logging
import logging.config

from django.core.exceptions import ObjectDoesNotExist

from products.models import Ingredient, Composition

logger = logging.getLogger(__name__)
fh = logging.FileHandler(os.path.join(os.getcwd(), 'ingredients.log'))
fh.setLevel(logging.WARNING)
logger.addHandler(fh)


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
