from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.forms import StreamForm
from apps.models import Category, Product, Stream


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


class MarketProductListView(LoginRequiredMixin, ListView):
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
            return super().get_queryset().filter(owner=self.request.user)


class StreamFormView(LoginRequiredMixin, FormView):
    form_class = StreamForm
    template_name = 'apps/product/market-products.html'

    def form_valid(self, form):
        print('valid', form.errors)
        if form.is_valid():
            form.save()
        return redirect('stream-list')

    def form_invalid(self, form):
        print('invalid', form.errors)
        return redirect('stream-list')

class StreamListVIew(ListView):
    queryset = Stream.objects.all()
    template_name = 'apps/product/oqimlarim.html'
    context_object_name = 'streams'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
