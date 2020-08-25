from django.urls import path
from . import views


urlpatterns = [
    path('summarize/', views.ArticleSummarization.predict_summarization),
]