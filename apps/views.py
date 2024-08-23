from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView

from apps.models import Category, Product, User


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
