import docx2txt
import os
import re
from pdfminer.high_level import extract_text
from streamlit.runtime.uploaded_file_manager import UploadedFile
from win32com import client
from win32com.client import constants


def process_doc_to_str(file: UploadedFile) -> str:
    docx_file_path = save_as_docx(file, "./data/temp.doc")
    with open(docx_file_path, "rb") as docx_file:
        return process_docx_to_str(docx_file)


def process_docx_to_str(file: UploadedFile) -> str:
    raw_text = docx2txt.process(file)
    processed_text = remove_blank_lines(raw_text)
    return processed_text


def process_pdf_to_str(file: UploadedFile) -> str:
    raw_text = extract_text(file)
    processed_text = remove_blank_lines(raw_text)
    return processed_text


def process_rtf_to_str(file: UploadedFile) -> str:
    docx_file_path = save_as_docx(file, "./data/temp.rtf")
    with open(docx_file_path, "rb") as docx_file:
        return process_docx_to_str(docx_file)


def save_as_docx(file: UploadedFile, temp_file_path: str) -> str:
    file_content = file.read()
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)
    word = client.gencache.EnsureDispatch("Word.Application")
    doc = word.Documents.Open(os.path.abspath(temp_file_path))
    doc.Activate()
    # Rename path with .docx
    new_file_abs = os.path.abspath(temp_file_path)
    new_file_abs = re.sub(r"\.\w+$", ".docx", new_file_abs)
    # Save and Close. Use wdFormatXMLDocument instead of wdFormatDocument
    word.ActiveDocument.SaveAs(new_file_abs, FileFormat=constants.wdFormatXMLDocument)
    doc.Close(False)
    return new_file_abs


def remove_blank_lines(input_str: str) -> str:
    # Split the string into lines, filter out blank lines, and join the non-blank lines back into a string
    lines = input_str.splitlines()
    non_blank_lines = [line for line in lines if line.strip()]
    return "\n".join(non_blank_lines)
