import os
from PyPDF2 import PdfFileReader


def find_word_in_txt(file_path, word):
    """Search for the word in a .txt file and return the line numbers where it was found."""
    with open(file_path, 'r') as file:  # 'file_path' should be the full path to the file
        lines = file.readlines()

    results = [i for i, line in enumerate(lines) if word in line]
    return results


def find_word_in_pdf(file_path, word):
    """Search for the word in a .pdf file and return the page numbers where it was found."""
    with open(file_path, 'rb') as file:
        pdf = PdfFileReader(file)
        results = []

        for i in range(pdf.getNumPages()):
            page = pdf.getPage(i)
            if word in page.extractText():
                results.append(i)

    return results


def find_word(file_path, word):
    """Choose the right function depending on the file's extension and execute it."""
    _, extension = os.path.splitext(file_path)

    if extension == '.txt':
        return find_word_in_txt(file_path, word)
    elif extension == '.pdf':
        return find_word_in_pdf(file_path, word)
