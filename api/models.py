from django.db import models, transaction
from document2text.models import Document
from .utils import break_large_text, generate_summary, generate_question

summary_max_token_limit = 10000
quest_max_token_limit = 2000
overlap = 50


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=200)


class Question(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    options = models.JSONField()
    answer = models.CharField(max_length=255)

    @classmethod
    def generate(cls, document_id):
        document = Document.objects.get(id=document_id)
        chunks = break_large_text(document.text, quest_max_token_limit)
        with transaction.atomic():
            for i, chunk in enumerate(chunks):
                print(f"chunk {i}: {chunk.strip()}")
                questions = generate_question(chunk)
                print(f"question {i}: {questions}")
                for question, choices, answer in questions:
                    question_obj = cls.objects.create(
                        document=document,
                        question=question,
                        options=choices,
                        answer=answer,
                    )
                    question_obj.save()
                i += 1

    def __str__(self):
        return f"Question {self.id} for Document {str(self.document)}"


# class Option(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     option = models.CharField(max_length=500)
#     isAnswer = models.BooleanField(default=False)


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
