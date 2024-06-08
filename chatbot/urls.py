from django.urls import path
from .views import sentiment_analysis, question_answering, summarize_text, translate_text_fr_en, translate_to_french

app_name = 'chatbot'

urlpatterns = [
    path('question_answering/', question_answering, name='question_answering'),
    path('sentiment_analysis/', sentiment_analysis, name="sentiment_analysis"),
    path('summarize_text/', summarize_text, name="summarize_text"),
    path('translate_fr_en/', translate_text_fr_en, name="translate_fr_en"),
    path('translate_en_fr/', translate_to_french, name='translate_en_fr'),
]
    