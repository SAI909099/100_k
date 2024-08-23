from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from apps.views import HomeView, ProductListView

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('product/list', ProductListView.as_view(), name='product_list'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
