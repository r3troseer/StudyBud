from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from document2text.models import Document

class FileSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields=['document']


class QuestionSerializer(ModelSerializer):
    pass


class SummarySerializer(ModelSerializer):
    pass


class FeedbackSerializer(ModelSerializer):
    pass