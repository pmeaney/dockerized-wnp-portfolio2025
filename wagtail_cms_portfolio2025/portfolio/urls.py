from django.urls import path
from .views import TagModalView

app_name = 'portfolio'

urlpatterns = [
    path('tag-modal/', TagModalView.as_view(), name='tag_modal'),
]