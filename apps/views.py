from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q
from django.views import View
from apps.models import Category, Product, User
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Order
import re


class HomeView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/home_page.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        return data

    def get_queryset(self):
        qs = super().get_queryset()
        if search := self.request.GET.get('search'):
            qs = qs.filter(Q(name__icontains=search) | Q(name__icontains=search))
        return qs


class CategoryListView(ListView):
    template_name = 'apps/home_page.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.kwargs.get('category_id')

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = queryset.filter(category=category)

        return queryset

    def get_template_names(self):
        if self.request.path == '/explore/':
            return ['apps/product/category_products.html']
        return ['apps/home_page.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset_(self):
        qs = super().get_queryset()
        if search := self.request.GET.get('search'):
            qs = qs.filter(Q(name__icontains=search) | Q(name__icontains=search))
        return qs


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


class CustomLoginView(TemplateView):
    template_name = 'apps/auth/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            user = User.objects.create_user(username=username, password=request.POST['password'])
            login(request, user)
            return redirect('home')
        else:
            user = authenticate(request, username=username, password=request.POST['password'])
            if user:
                login(request, user)
                return redirect('home')

            else:
                context = {
                    "messages_error": ["Invalid password"]
                }
                return render(request, template_name='apps/auth/login.html', context=context)


# def explore_products(request):
#     products = Product.objects.all()
#     context = {
#         'products': products,
#     }
#     return render(request, 'apps/product/category_products.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class OrderSuccessView(View):
    product = Product.objects.all()

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, template_name='apps/order_success.html',
                      context={'order': order, 'products': self.product})


class CreateOrderView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'apps/product_detail.html', {'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        order = Order(
            name=request.POST.get('full_name'),
            phone_number=re.sub(r'\D', '', request.POST.get('phone_number')),
            region_name=request.POST.get('region_name'),
            product=product
        )
        try:
            order.clean()
        except ValidationError as e:
            context = {
                "messages_error": [e.message],
                "product": product
            }
            return render(request, 'apps/product_detail.html', context=context)

        order.save()
        return redirect('order_success', order_id=order.id)

class MarketProductListView(LoginRequiredMixin,ListView):
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

