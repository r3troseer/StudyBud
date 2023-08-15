from rest_framework import generics, status, views, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from document2text.models import Document
from .serializers import (
    FileSerializer,
    SummarySerializer,
    QuestionSerializer,
    FeedbackSerializer,
)
from .pagination import QuestionPagination
from .tasks import generate_and_append_chunks
from .models import Summary, Question, Feedback


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
    """
    API endpoint to generate a summary.

    - Retrieves the Document object based on the provided primary key.
    - Generates a summary for the document's text.
    - Returns the summary in the response.
    """

    queryset = Summary.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SummarySerializer

    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            print(document)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND
            )
        summary = Summary.objects.create(document=document)
        summary.generate()
        serializer = self.get_serializer(summary)
        return Response(serializer.data)


class GenerateQuestionsView(generics.GenericAPIView):
    """
    API endpoint to generate questions.

    - Retrieves the Document object based on the provided primary key.
    - Generates aquestions for the document's text.
    - Returns the questions in the response.
    """

    permission_classes = [AllowAny]
    serializer_class = QuestionSerializer

    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND
            )
        questions = Question.generate(document.id)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)


class GenerateQuestionsDelayView(views.APIView):
    """
    API endpoint to generate questions.

    - Initiates a task to generate questions for a specified document.
    - Returns a message indicating the task has started.
    """

    def post(self, request, *args, **kwargs):
        document_id = request.data.get("document_id")
        generate_and_append_chunks.delay(document_id)
        return Response(
            {"message": "Question generation task started."}, status=status.HTTP_200_OK
        )


class QuestionListView(generics.ListAPIView):
    """
    API endpoint to retrieve questions.

    - Retrieves and returns a list of questions for a specific document.
    """

    serializer_class = QuestionSerializer
    pagination_class = QuestionPagination

    def get_queryset(self):
        document_id = self.request.query_params.get("document_id")
        return Question.objects.filter(document_id=document_id)


class FeedbackView(generics.CreateAPIView):
    """
    API endpoint to generate feedback.

    - Retrieves the Question object based on the provided primary key.
    - Generates a feeback for the document's text.
    - Returns the feedback in the response.
    """

    queryset = Feedback.objects.all()
    permission_classes = [AllowAny]
    serializer_class = FeedbackSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]
        wrong_answer = serializer.validated_data.get("wrong_answer", None)

        feedback = Feedback(question=question)
        feedback.generate(wrong_answer=wrong_answer)
        feedback.save()

        response_data = serializer.data
        response_data["feedback_text"] = feedback.feedback_text

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=201, headers=headers)
