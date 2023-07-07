from django.db import models
from document2text.models import Document


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=200)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=500)
    isAnswer = models.BooleanField(default=False)


class Summary(models.Model):
    text = models.ForeignKey(Document, on_delete=models.CASCADE)
    summarized_text = models.TextField()

    class Meta:
        verbose_name_plural = "summaries"

    def __str__(self):
        return self.text
