from celery import shared_task
from .models import Question


@shared_task()
def generate_and_append_chunks(document_id):
    """
    Task to generate and append chunks of questions
    """
    print("started")
    question = Question.generate(document_id)
    print("in progress")
    print(question)
