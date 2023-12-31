# StudyBud


StudyBud is an AI-driven learning tool that enhances the learning experience for students and educators. It leverages OpenAI's API to provide advanced features such as question generation, summarization, and Feedback. The tool allows users to upload PDF and DOCX files, extract text content, generate questions, create summaries, and receive Feedback based on their performance.

## Features

- User-friendly web interface for file upload and processing, quiz and summary view.
- Supports PDF and DOCX file formats.
- Extracts text content from uploaded files.
- Generates a variety of questions to test user understanding.
- Summarizes content for easier review and retention.
- Provides Feedback based on performance.
## Prerequisites

- Python 3.11
- Django 4.2.2
- PyMuPDF (for PDF text extraction)
- docx2txt (for DOCX text extraction)
- Python-magic (optional)
- nltk

## Installation

1. Clone the repository to your local machine:
```
git clone https://github.com/r3troseer/StudyBud.git
```

2. Install the required Python packages:
```
pip install -r requirements.txt
```

3. Migrate the database:
```
python manage.py migrate
```

4. Run the development server:
```
python manage.py runserver
```

5. Open your web browser and go to http://localhost:8000/ to view the application.
