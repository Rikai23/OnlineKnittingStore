from urllib.parse import urlencode
from django.core.cache import cache
from django import template
from goods.models import Categories

register = template.Library()

@register.simple_tag
def tag_categories():
    categories = cache.get('categories_list')

    if categories is None:
        categories = Categories.objects.all()
        cache.set('categories_list', categories, 60 * 60)

    return categories

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)