from django.urls import path, include

from .views import FileView, SummaryView, GenerateQuestionsDelayView, QuestionListView, GenerateQuestionsView

urlpatterns = [
    path("file/", FileView.as_view()),
    path('summaries/<int:pk>/generate_summary/', SummaryView.as_view(), name='generate-summary'),
    path('questions/<int:pk>/generate_question/', GenerateQuestionsView.as_view(), name='generate-summary'),
    path('generate-questions/', GenerateQuestionsDelayView.as_view(), name='generate-questions'),
    path('questions/', QuestionListView.as_view(), name='question-list'),

]
