import docx2txt
import fitz
import os
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False
# print(HAS_MAGIC)

ALLOWED_MIME_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]
ALLOWED_EXTENSIONS = [".pdf", ".docx"]


def validate_file_type(value):
    """
    Custom file type validation based on presence of 'magic' module or file extension
    """
    if HAS_MAGIC:
        print("magic")
        file_type = magic.from_buffer(value.read(), mime=True)
        print(file_type)
        if file_type not in ALLOWED_MIME_TYPES:
            raise ValidationError(
                "Invalid file type. Only PDF and DOCX files are allowed."
            )
    else:
        print("no magic")
        ext = os.path.splitext(value.name)[1]
        if ext.lower() not in ALLOWED_EXTENSIONS:
            raise ValidationError(
                "Invalid file type. Only PDF and DOCX files are allowed."
            )


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    document = models.FileField(upload_to="documents/", validators=[validate_file_type])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def process_file(self):
        """
        Process the uploaded file based on its file type
        """
        if HAS_MAGIC:
            if magic.from_buffer(self.read(), mime=True) == "application/pdf":
                self.process_pdf()
            elif (
                magic.from_buffer(self.read(), mime=True)
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                self.process_word()
        else:
            ext = os.path.splitext(self.document.name)[1]
            if ext.lower() == ".pdf":
                self.process_pdf()
            elif ext.lower() == ".docx":
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
        Returns the content of the file
        """
        reading = self.document.read()
        self.document.seek(0)  # Resets file pointer
        return reading

    def name(self):
        """
        Returns only the filename without the 'document/' prefix.
        """
        return os.path.basename(self.document.name)

    def __str__(self):
        return self.name()
