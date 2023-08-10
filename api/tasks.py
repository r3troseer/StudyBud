from celery import shared_task, current_task
from .models import Question



@shared_task()
def generate_and_append_chunks(document_id):
    print('started')
    question = Question.generate(document_id)
    print("in progress")
    print(question)
