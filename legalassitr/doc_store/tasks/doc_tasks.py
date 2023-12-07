import zipfile
import pdfkit
import html2text
from celery import shared_task
from io import BytesIO
from django.core.files.base import ContentFile
from docx import Document as DocxDocument


@shared_task
def compress_document(document):
    try:
        with document.file.open('rb') as file:
            compressed_content = BytesIO()
            with zipfile.ZipFile(compressed_content, 'w') as zip_file:
                zip_file.write(file.read(), document.title + '.' + document.file.name.split('.')[-1])

        document.compressed_file.save(f"{document.title}.zip", ContentFile(compressed_content.getvalue()))
        document.save()
    except Exception as ex:
        raise Exception(f"Error compressing document contents : {str(ex)}")

@shared_task
def convert_to_pdf(html_content):
    try:
        options = {'page-size': 'A4', 'encoding': 'UTF-8'}
        pdf_content = pdfkit.from_string(html_content, False, options=options)
        return pdf_content
    except Exception as ex:
        raise Exception(f"Error generating PDF : {str(ex)}")

@shared_task
def convert_to_word(html_content):
    try:
        text_content = html2text.html2text(html_content)
        document = DocxDocument()
        document.add_paragraph(text_content)

        buffer = BytesIO()
        document.save(buffer)

        return buffer.getvalue()
    except Exception as ex:
        raise Exception(f"Error generating Word document : {str(ex)}")