from django.urls import path
from . import views

urlpatterns = [
    path('api/summarize', views.ArticleSummarization.as_view()),
    path('api/category', views.ArticleCategory.as_view()),
]