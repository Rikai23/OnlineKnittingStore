from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

from goods.models import Products, Categories


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    sort = request.GET.get('sort', None)
    query = request.GET.get('q', '').strip()

    if category_slug == 'all':
        goods = Products.objects.all()
        category_name = "Все товары"
    elif category_slug == 'sale':
        goods = Products.objects.filter(discount__gt=0)
        category_name = "Распродажа"
    else:
        goods = Products.objects.filter(category__slug=category_slug)
        if not goods.exists():
            raise Http404("Товары для этой категории не найдены")
        category = Categories.objects.get(slug=category_slug)
        category_name = category.name

    if query:
        goods = goods.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if sort == 'date_desc':
        goods = goods.order_by('-id')  # новые → старые
    elif sort == 'date_asc':
        goods = goods.order_by('id')  # старые → новые

    paginator = Paginator(goods, 9)
    current_page = paginator.page(int(page))

    context = {
        'title': category_name,
        'goods': current_page,
        'category_slug': category_slug,
        'search_query': query,
        'sort_value': sort,
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)
    context = {
        'title': product.name,
        "product": product,
    }
    return render(request, 'goods/product.html', context)

