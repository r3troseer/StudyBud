from django.db import models
from document2text.models import Document
from time import sleep
from .utils import (
    break_large_text,
    generate_summary,
    generate_question,
    quest_parser,
    generate_feedback,
)

summary_max_token_limit = 10000
quest_max_token_limit = 2000
overlap = 50


class Question(models.Model):
    """Model to store generated questions"""

    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=512, null=True)
    options = models.JSONField(null=True)
    answer = models.CharField(max_length=512, null=True)

    @classmethod
    def generate(cls, document_id):
        """
        Generate questions and store them in the database
        """
        document = Document.objects.get(id=document_id)
        chunks = break_large_text(document.text, quest_max_token_limit)
        number_of_chunks = len(chunks)
        quiz = []
        for i, chunk in enumerate(chunks):
            quest = generate_question(chunk)
            questions = quest_parser(quest)
            question_objs = []
            for question, choices, answer in questions:
                question_obj = cls(
                    document=document,
                    question=question,
                    options=choices,
                    answer=answer,
                )
                question_objs.append(question_obj)

            quiz_obj = cls.objects.bulk_create(question_objs)
            quiz.extend(quiz_obj)
            if number_of_chunks > 2:
                sleep(10)
        return quiz

    def __str__(self):
        return f"Question {self.id} for Document {str(self.document)}"


class Summary(models.Model):
    """Model to store generated summary"""

    summarized_text = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "summaries"

    def generate(self):
        """
        Generate summaries by chunk and append to summarized_text
        """
        chunks = break_large_text(self.document.text, summary_max_token_limit)

        for i, chunk in enumerate(chunks):
            summary = generate_summary(chunk)
            self.summarized_text += summary
            i += 1
        self.save()

    def __str__(self):
        return str(self.document)


class Feedback(models.Model):
    """Model to store generated Feedback"""

    feedback_text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    wrong_answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "feedbacks"

    def generate(self, wrong_answer):
        """
        Generate feedback based on question and wrong answer
        """
        self.wrong_answer=wrong_answer
        feedback = generate_feedback(
            self.question.question, self.question.answer, self.wrong_answer
        )
        self.feedback_text = feedback
        self.save()

    def __str__(self):
        return f'{self.feedback_text} for {str(self.question)}'
