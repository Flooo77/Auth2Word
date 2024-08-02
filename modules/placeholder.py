"""
This module provides functionality for extracting placeholders from a Word document
template.

Placeholders are defined as text enclosed in square brackets (e.g., [PLACEHOLDER]). 
The module searches for these placeholders in both the text of paragraphs and in 
table cells within the document.

Functions:
- get_placeholders: Extracts unique placeholders from the specified Word document, 
                    checking both paragraphs and tables.
"""

import re
from docx import Document

def get_placeholders(template_path):
    """
    Extracts placeholders from a Word document template.

    Placeholders are defined as text enclosed in square brackets (e.g., [PLACEHOLDER]). 
    This function searches both paragraph texts and table cell texts in the document.

    Args:
        template_path (str): The file path to the Word document template.

    Returns:
        list: A list of unique placeholders found in the document, with duplicates removed.
    """

    doc = Document(template_path)
    placeholders = set()

    for paragraph in doc.paragraphs:
        placeholders.update(re.findall(r'\[([A-Z_]+)\]', paragraph.text))

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    placeholders.update(re.findall(r'\[([A-Z_]+)\]', paragraph.text))

    return list(placeholders)
