from django.shortcuts import render
from rest_framework import generics, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from document2text.models import Document
from .serializers import FileSerializer,SummarySerializer
from .models import Summary


class FileView(generics.GenericAPIView):
    """
    API endpoint to upload and process a file.

    - Validates the file using the serializer.
    - Creates a new Document object with the uploaded file.
    - Processes the file and extracts text based on its type.
    - Returns the response with the created Document details.
    """

    queryset = Document.objects.all()
    permission_classes = [AllowAny]
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data["document"]
            document = Document.objects.create(document=file)
            document.process_file()
            response_data = {
                "id": document.id,
                "name": document.name(),
            }

            message = {"detail": "File analyzed."}
            return Response(
                {**response_data, **message}, status=status.HTTP_201_CREATED
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SummaryView(generics.GenericAPIView):
    queryset = Summary.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SummarySerializer

    def get(self, request, pk):

        try:
            document = Document.objects.get(pk=pk)
            print(document)
        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)

        summary = Summary.objects.create(document=document)
        summary.generate()

        serializer = self.get_serializer(summary)
        return Response(serializer.data)
# class QuizView(generics):
#     pass

# class SummaryView(generics):
#     pass

# class FeedbackView(generics):
#     pass
