from django.urls import path
from .views import chatbot_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('chat/', chatbot_view, name='chatbot_view'),
    # path('index/', chatbot_view, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)