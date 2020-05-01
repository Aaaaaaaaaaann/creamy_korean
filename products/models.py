from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify


class Section(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.DO_NOTHING, related_name='children')
    slug = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.TextField(unique=True)
    brand = models.TextField()
    volume = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, blank=True, null=True, related_name='products')
    slug = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SectionTemp(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='section_temp')
    section = ArrayField(models.CharField(max_length=25), blank=True, null=True)

    def __str__(self):
        return self.section


class IngredientsGroup(models.Model):

    class Kind(models.TextChoices):
        UNDESIRABLE = 'нежелательные'
        ACTIVE = 'активные'

    name = models.TextField(unique=True)
    kind = models.CharField(max_length=50, choices=Kind.choices, blank=True, null=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.TextField(unique=True)
    function = models.TextField(blank=True, null=True)
    group = models.ForeignKey(IngredientsGroup, on_delete=models.DO_NOTHING, blank=True, null=True,
                              related_name='ingredients')


class Composition(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='composition')
    ingredients = ArrayField(models.IntegerField(), blank=True, null=True)


class CompositionTemp(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='composition_temp')
    ingredients = ArrayField(models.TextField(), blank=True, null=True)
    processed = models.BooleanField(default=False)


class Shop(models.Model):
    name = models.TextField(unique=True)
    link = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    available_regions = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    free_courier_delivery = models.TextField(blank=True, null=True)
    link_to_delivery_conditions = models.TextField(blank=True, null=True)


class ProductInShop(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='available_in_shops', blank=True, null=True)
    availability = models.BooleanField(default=True)
    current_price = models.IntegerField(blank=True, null=True)
    link_to_product_page = models.TextField(blank=True, null=True)
