from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from apps.views import HomeView, ProductListView, MarketProductListView, ProductDetailView

urlpatterns = [
    path('aaa', HomeView.as_view(), name='home'),
    path('product-list', ProductListView.as_view(), name='product-list'),
    path('', MarketProductListView.as_view(), name='market_product_list'),
    path('product_detail',ProductDetailView.as_view(), name='product_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
document_root = settings.STATIC_ROOT)

