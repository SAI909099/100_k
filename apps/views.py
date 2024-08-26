from django.views.generic import ListView, DetailView

from apps.models import Category, Product


class HomeView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/home_page.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        return data


class CategoryListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/home_page.html'
    # context_object_name = 'products'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['categories'] = Category.objects.all()
        # data['products'] = Product.objects.all()

        return data


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        cat_slug = self.request.GET.get("category")
        query = super().get_queryset()
        if cat_slug:
            query = query.filter(category__slug=cat_slug)
        return query

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data

class MarketProductListView(ListView):
    model = Product
    template_name = 'apps/product/market-products.html'
    context_object_name = 'products'

    def get_queryset(self):
        sort_by = self.request.GET.get('sort', 'newest')

        if sort_by == 'newest':
            return Product.objects.all().order_by('-created_at')
        elif sort_by == 'top_selling':
            return Product.objects.all().order_by('-sold_count')
        elif sort_by == 'quantity':
            return Product.objects.all().order_by('-quantity')
        else:
            return Product.objects.all()


class ProductDetailView(DetailView):
    pass