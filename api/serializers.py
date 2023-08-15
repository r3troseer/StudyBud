from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Summary, Question, Feedback
from document2text.models import Document
import re


class FileSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ["document"]


class QuestionSerializer(ModelSerializer):
    correct_answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        # fields = "__all__"
        exclude = ["answer"]

    def get_correct_answer(self, obj):
        options = obj.options
        answer = obj.answer
        try:
            correct_index = options.index(answer)
        except ValueError:
            # Extract the first part (letter)
            answer_parts = re.split(r"[).]", answer)
            answer_letter = answer_parts[0].strip()

            option_letters = [
                re.split(r"[).]", option)[0].strip() for option in options
            ]
            correct_index = option_letters.index(answer_letter)

        return correct_index


class SummarySerializer(ModelSerializer):
    class Meta:
        model = Summary
        fields = ["document", "summarized_text"]


class FeedbackSerializer(ModelSerializer):
    wrong_answer = serializers.CharField(write_only=True)
    feedback_text = serializers.CharField(read_only=True)

    class Meta:
        model = Feedback
        fields = ["question", 'feedback_text', 'wrong_answer']

    