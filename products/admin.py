from django.contrib import admin


from .models import Section, IngredientsGroup, Ingredient, Shop


class SectionInline(admin.TabularInline):
    model = Section
    can_delete = False


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent',)
    list_filter = ('parent',)
    ordering = ('parent',)
    inlines = (SectionInline,)
    list_display_links = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group')
    list_filter = ('group',)
    ordering = ('name',)


class IngredientInline(admin.TabularInline):
    model = Ingredient
    fields = ('name', 'group')
    can_delete = False


@admin.register(IngredientsGroup)
class IngredientsGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    inlines = (IngredientInline,)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name',)
