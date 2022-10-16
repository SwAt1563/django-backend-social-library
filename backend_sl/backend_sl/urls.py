"""backend_sl URL Configuration


"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# when use the api be careful with the last slash '/' u should put it
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('profile/', include('user_profile.urls', namespace='user_profile')),
    path('friend/', include('friend.urls', namespace='friend')),
    path('notification/', include('notification.urls', namespace='notification')),
    path('post/', include('post.urls', namespace='post')),
    path('admin_app/', include('admin_app.urls', namespace='admin_app')),
]

# for confirm the static paths
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)