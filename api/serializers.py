from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Summary, Question
from document2text.models import Document


class FileSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ["document"]


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class SummarySerializer(ModelSerializer):
    class Meta:
        model = Summary
        fields = ["document", "summarized_text"]


class FeedbackSerializer(ModelSerializer):
    pass
