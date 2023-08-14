from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from document2text.models import Document
from api.models import Question, Summary
from django.contrib.auth.models import User

text = """A requirement can be any need or expectation for a system or for its software. Requirements reflect the stated or implied needs of the customer, and may be market-based, contractual, or statutory, as well as an organization's internal requirements. 
There can be many different kinds of requirements (e.g., design, functional, implementation, interface, performance, or physical requirements). Software requirements are typically derived from the system requirements for those aspects of system functionality that have been allocated to software. 
Software requirements are typically stated in functional terms and are defined, refined, and updated as a development project progresses. Success in accurately and completely documenting software requirements is a crucial factor in successful validation of the resulting software.
"""


class DocumentProcessingTestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create(username="testuser", password="testpassword")

    def test_file_upload_and_text_extraction(self):
        # client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Upload a sample PDF or DOCX file
        file_path = "C:/Users/user/Documents/StudyMate/documents/PROJECT_REPORT.docx"
        with open(file_path, "rb") as file:
            response = self.client.post(
                reverse("file-upload"), {"document": file}, format="multipart"
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        document_id = response.data["id"]

        # Retrieve the processed document
        document = Document.objects.get(id=document_id)
        self.assertTrue(document.text)  # Ensure that text extraction was successful

    def test_summary_generation(self):
        # Create a sample document
        document = Document.objects.create(user=self.user, text="Sample document text")

        # Generate a summary
        summary = Summary.objects.create(document=document)
        summary.generate()

        # Retrieve the generated summary
        generated_summary = Summary.objects.get(id=summary.id)
        self.assertTrue(
            generated_summary.summarized_text
        )  # Ensure that a summary was generated

    def test_question_generation(self):
        # Create a sample document
        document = Document.objects.create(user=self.user, text=text)

        # Generate questions from the document
        Question.generate(document.id)

        # Retrieve the generated questions
        generated_questions = Question.objects.filter(document=document)
        self.assertTrue(generated_questions)  # Ensure that questions were generated


class APIViewsTestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create(username="testuser", password="testpassword")

    def test_file_upload_api(self):
        # client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Upload a sample PDF or DOCX file
        file_path = "C:/Users/user/Documents/StudyMate/documents/PROJECT_REPORT.docx"
        with open(file_path, "rb") as file:
            response = self.client.post(
                reverse("file-upload"), {"document": file}, format="multipart"
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        document_id = response.data["id"]

        # Retrieve the processed document
        document = Document.objects.get(id=document_id)
        self.assertTrue(document.text)  # Ensure that text extraction was successful

    def test_summary_generation_api(self):
        # Create a sample document
        document = Document.objects.create(user=self.user, text=text)

        # Generate a summary using the API view
        response = self.client.get(
            reverse("generate-summary", kwargs={"pk": document.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        generated_summary = Summary.objects.get(document=document)
        self.assertTrue(
            generated_summary.summarized_text
        )  # Ensure that a summary was generated

    def test_question_generation_api(self):
        # Create a sample document
        document = Document.objects.create(user=self.user, text=text)

        # Generate questions using the API view
        response = self.client.get(
            reverse("generate-questions", kwargs={"pk": document.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        generated_questions = Question.objects.filter(document=document)
        self.assertTrue(generated_questions)  # Ensure that questions were generated

    def test_question_generation_task_api(self):
        # Create a sample document
        document = Document.objects.create(user=self.user, text=text)

        # Generate questions using the API view
        response = self.client.post(
            reverse("generate-questions-task"),
            {"document_id": document.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
