from django.urls import path
from .views import SpeakerListView, NewsListView, RegistrationViewSet

urlpatterns = [
    path('api/speakers/', SpeakerListView.as_view(), name='speaker-list'),
    path('api/news/', NewsListView.as_view(), name='news-list'),
    path('api/registration/', RegistrationViewSet.as_view({'post': 'create', 'get': 'list'}), name='registration-list-create'),
]
