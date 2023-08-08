from django.urls import path, include

from .views import FileView, SummaryView

urlpatterns = [
    path("file/", FileView.as_view()),
    path('summaries/<int:pk>/generate_summary/', SummaryView.as_view(), name='generate-summary')
]
