from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from document2text.models import Document
from .serializers import FileSerializer


class FileView(generics.GenericAPIView):
    queryset = Document.objects.all()
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data["document"]
            document = Document.objects.create(document=file)
            document.process()
            message = {"detail": ("File analyzed.")}
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class QuizView(generics):
#     pass

# class SummaryView(generics):
#     pass

# class FeedbackView(generics):
#     pass
