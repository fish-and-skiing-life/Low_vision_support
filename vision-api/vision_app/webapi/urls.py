from django.urls import path
from . import views

urlpatterns = [
    path('api/summarize', views.Summarization.as_view()),
    path('api/recommend', views.Recommendation.as_view()),
    path('api/category', views.ArticleCategory.as_view()),
    path('api/article_list', views.ArticleList.as_view()),
    path('api/wiki', views.Wikipedia.as_view()),
    path('api/calcDb', views.CalcDb.as_view()),
    path('api/calcTrend', views.CalcTrend.as_view()),
    path('api/insertwiki', views.InsertWiki.as_view()),
]
