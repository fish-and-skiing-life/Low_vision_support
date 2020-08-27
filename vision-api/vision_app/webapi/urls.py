from django.urls import path
from . import views

urlpatterns = [
    path('api/summarize', views.ArticleSummarization.as_view()),
]