from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from apps.views import HomeView, ProductListView, MarketProductListView, StreamFormView, StreamListVIew

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('product/list', ProductListView.as_view(), name='product_list'),
                  path('market/', MarketProductListView.as_view(), name='market_list'),

                  path('stream/form', StreamFormView.as_view(), name='stream-form'),
                  path('stream/list', StreamListVIew.as_view(), name='stream-list'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
