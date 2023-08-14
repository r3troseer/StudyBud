from django.urls import path, include

from .views import FileView, SummaryView, GenerateQuestionsDelayView, QuestionListView, GenerateQuestionsView

urlpatterns = [
    path("file/", FileView.as_view(), name='file-upload'),
    path('summaries/<int:pk>/generate_summary/', SummaryView.as_view(), name='generate-summary'),
    path('questions/<int:pk>/generate_question/', GenerateQuestionsView.as_view(), name='generate-questions'),
    path('generate-questions/', GenerateQuestionsDelayView.as_view(), name='generate-questions-task'),
    path('questions/', QuestionListView.as_view(), name='question-list'),

]
