from django.db import models, transaction
from document2text.models import Document
from time import sleep
from .utils import break_large_text, generate_summary, generate_question, quest_parser

summary_max_token_limit = 10000
quest_max_token_limit = 2000
overlap = 50


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=200)


class Question(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=255, null=True)
    options = models.JSONField(null=True)
    answer = models.CharField(max_length=255, null=True)

    @classmethod
    def generate(cls, document_id):
        document = Document.objects.get(id=document_id)
        chunks = break_large_text(document.text, quest_max_token_limit)
        number_of_chunks = len(chunks)
        # with transaction.atomic():
        for i, chunk in enumerate(chunks):
            # print(f"chunk {i}: {chunk.strip()}")
            quest = generate_question(chunk)
            # print(f"question {i}: {quest}")
            questions = quest_parser(quest)
            print(questions)
            question_objs = []
            for question, choices, answer in questions:
                question_obj = cls(
                    document=document,
                    question=question,
                    options=choices,
                    answer=answer,
                )
                question_objs.append(question_obj)

            cls.objects.bulk_create(question_objs)
            if number_of_chunks > 2:
                sleep(10)

    def __str__(self):
        return f"Question {self.id} for Document {str(self.document)}"


class Summary(models.Model):
    summarized_text = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "summaries"

    def generate(self):
        chunks = break_large_text(self.document.text, summary_max_token_limit)

        for i, chunk in enumerate(chunks):
            print(f"chunk {i}: {chunk.strip()}")
            summary = generate_summary(chunk)
            print(f"summary {i}: {summary}")
            self.summarized_text += summary + "\nend\n"
            i += 1
        self.save()

    def __str__(self):
        return str(self.document)
