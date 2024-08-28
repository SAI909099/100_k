from unicodedata import category

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.views import HomeView, ProductListView, CustomLoginView, CategoryListView, ProductDetailView, \
    OrderSuccessView, CreateOrderView, AdminDashboardView, ProfileView, AdminMarketView, \
    AdminStatisticsView, AdminStreamView, AdminPaymentView, ProductSearchView, AllView  # MarketProductListView

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
                  path('product/detail/<str:slug>', ProductDetailView.as_view(), name='pro_detail'),
                  path('create/order/<int:product_id>', CreateOrderView.as_view(), name='create_order'),
                  path('order/success/<int:order_id>', OrderSuccessView.as_view(), name='order_success'),

                  path('contacts', AdminDashboardView.as_view(), name='contacts'),
                  path('login/', CustomLoginView.as_view(), name='login'),
                  path('logout', LogoutView.as_view(), name='logout'),
                  path('admin1/profile', ProfileView.as_view(), name='profile'),
                  path('admin1/', AdminDashboardView.as_view(), name='dashboard'),
                  path('admin1/market', AdminMarketView.as_view(), name='market'),
                  path('admin1/statistics', AdminStatisticsView.as_view(), name='statistics'),
                  path('admin1/stream', AdminStreamView.as_view(), name='stream'),
                  path('admin1/payment', AdminPaymentView.as_view(), name='payment'),
                  path('admin1/profile', ProfileView.as_view(), name='profile'),
                  path('search/', ProductSearchView.as_view(), name='product_search'),
                  path('all_products/', AllView.as_view(), name='all_products'),

                  # path('market/', MarketProductListView.as_view(), name='market_list'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
