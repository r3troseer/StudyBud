from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Summary, Question
from document2text.models import Document


class FileSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = ["document"]


class QuestionSerializer(ModelSerializer):
    correct_answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        # fields = "__all__"
        exclude = ['answer']

    def get_correct_answer(self, obj):
        options = obj.options
        answer = obj.answer
        try:
            correct_index = options.index(answer)
        except ValueError:
            # Extract the first part (letter)
            answer_letter = answer.split('.')[0].strip()
            option_letters = [option.split('.')[0].strip() for option in options]
            correct_index = option_letters.index(answer_letter)
            
        return correct_index


class SummarySerializer(ModelSerializer):
    class Meta:
        model = Summary
        fields = ["document", "summarized_text"]


class FeedbackSerializer(ModelSerializer):
    pass
