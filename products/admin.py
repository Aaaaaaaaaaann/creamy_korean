from django.contrib import admin


from .models import Section, IngredientsGroup, Ingredient, Shop


class SectionInline(admin.TabularInline):
    model = Section
    can_delete = False


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'slug')
    list_filter = ('parent',)
    ordering = ('parent',)
    inlines = (SectionInline,)
    list_display_links = ('name',)


class IngredientInline(admin.TabularInline):
    model = Ingredient
    fields = ('name', 'function')
    can_delete = False


@admin.register(IngredientsGroup)
class IngredientsGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind')
    list_filter = ('name', 'kind')
    inlines = (IngredientInline,)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name',)
