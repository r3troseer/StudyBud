import docx2txt
import fitz
import magic
from django.core.exceptions import ValidationError
from django.db import models


class Document(models.Model):
    text = models.TextField()
    document = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        self.validate_file_type()

    def validate_file_type(self):
        file_type = magic.from_buffer(self.read(), mime=True)
        if file_type not in [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]:
            raise ValidationError(
                "Invalid file type. Only PDF and DOCX files are allowed."
            )

    def process(self):
        self.clean()  # Perform file type validation before saving
        if magic.from_buffer(self.read(), mime=True) == "application/pdf":
            self.process_pdf()
        elif (
            magic.from_buffer(self.read(), mime=True)
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            self.process_word()

    def process_pdf(self):
        """
        Extracts text from PDF files
        """

        pdf = fitz.open(self.document)
        text = ""
        for page in pdf:
            text += page.get_text()
        self.text = text
        self.save()

    def process_word(self):
        """
        Extracts text from DOCX files
        """
        text = docx2txt.process(self.document)
        self.text = text
        self.save()

    def read(self):
        """
        method to return the content of the file
        """
        reading = self.document.read()
        self.document.seek(0)  # Resets file pointer
        return reading

    def __str__(self):
        return self.document.name
