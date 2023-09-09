from django.urls import path
from rest_framework.authtoken import views
from .views import BoxCreateView, BoxUpdateView, BoxListView, MyBoxListView, BoxDeleteView

urlpatterns = [
    path('add-box/', BoxCreateView.as_view(), name='add-box'),
    path('update-box/<int:pk>/', BoxUpdateView.as_view(), name='update-box'),
    path('list-boxes/', BoxListView.as_view(), name='list-boxes'),
    path('list-my-boxes/', MyBoxListView.as_view(), name='list-my-boxes'),
    path('delete-box/<int:pk>/', BoxDeleteView.as_view(), name='delete-box'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
]
