from unicodedata import category

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.views import HomeView, ProductListView, CustomLoginView, CategoryListView, ProductDetailView, \
    OrderSuccessView, CreateOrderView  #MarketProductListView

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('product-list', ProductListView.as_view(), name='product-list'),
                  path('login/', CustomLoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),

                  path('explore/<int:category_id>/', CategoryListView.as_view(), name='category_products'),
                  path('explore/', CategoryListView.as_view(), name='all_products'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),

                  path('product/list', ProductListView.as_view(), name='product_list'),
                  path('product/detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
                  path('create/order/<int:product_id>', CreateOrderView.as_view(), name='create_order'),
                  path('order/success/<int:order_id>', OrderSuccessView.as_view(), name='order_success'),

                  # path('market/', MarketProductListView.as_view(), name='market_list'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
