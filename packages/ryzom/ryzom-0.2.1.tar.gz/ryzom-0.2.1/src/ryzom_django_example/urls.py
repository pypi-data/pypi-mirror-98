from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('', include('ryzom_django_example.views')),
]

if settings.CHANNELS_ENABLE:
    urlpatterns.append(
        path('reactive/', include('ryzom_django_channels_example.views')),
    )
