from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.views import HomeView, ProductListView, CustomLoginView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product-list', ProductListView.as_view(), name='product-list'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
document_root = settings.STATIC_ROOT)
                  path('', HomeView.as_view(), name='home'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('product/list', ProductListView.as_view(), name='product_list'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
