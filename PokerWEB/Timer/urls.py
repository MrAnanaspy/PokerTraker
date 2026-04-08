from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

urlpatterns = [
    path('tournament/timer/<int:id>', get_timer, name='get-timer'),
    path('timer-data/<int:id>/', get_timer_data, name='get_timer_data'),
    path('api/knockout/', knockout, name='knockout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)