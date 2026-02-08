from django.db.models import Q
from django.http import Http404
from django.views.generic import DetailView, ListView

from goods.models import Products, Categories

class CatalogView(ListView):
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 9
    allow_empty = False

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        sort = self.request.GET.get('sort', None)
        query = self.request.GET.get('q', '').strip()

        if category_slug == 'all':
            goods = Products.objects.all()
        elif category_slug == 'sale':
            goods = Products.objects.filter(discount__gt=0)
        else:
            goods = Products.objects.filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404("Товары для этой категории не найдены")

        if query:
            goods = goods.filter(Q(name__icontains=query) | Q(description__icontains=query))

        if sort == 'date_desc':
            goods = goods.order_by('-id')  # новые → старые
        elif sort == 'date_asc':
            goods = goods.order_by('id')  # старые → новые

        return goods


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')

        if category_slug == 'all':
            category_name = 'Все товары'
        elif category_slug == 'sale':
            category_name = 'Распродажа'
        else:
            category = Categories.objects.get(slug=category_slug)
            category_name = category.name

        context['title'] = category_name
        context['category_slug'] = category_slug
        context['search_query'] = self.request.GET.get('q', '')
        context['sort_value'] = self.request.GET.get('sort')
        return context


class ProductView(DetailView):
    model = Products
    context_object_name = 'product'
    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context
