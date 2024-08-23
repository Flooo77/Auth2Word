"""
This module provides functions for generating and modifying Word documents using the `docx`
library.

Functions:
- replace_placeholder: Replaces placeholders in a paragraph with specified text.
- add_tabless: Adds a table to the document based on provided data.
- create_report: Creates a report from a template document, replaces placeholders, and saves 
                 the final document.
"""

import os

from docx import Document


def replace_placeholder(paragraph, placeholder, replacement):
    """
    Replaces a placeholder in a paragraph with the given replacement text.

    Args:
        paragraph (docx.text.paragraph.Paragraph): The paragraph where the placeholder will be
        replaced.
        placeholder (str): The placeholder text to be replaced.
        replacement (str): The text to replace the placeholder with.
    """

    if placeholder in paragraph.text:
        if placeholder in paragraph.text:
            inline = paragraph.runs
            for item in inline:
                if placeholder in item.text:
                    item.text = item.text.replace(placeholder, replacement)

def add_tables(doc, data):
    """
    Adds a table to the document based on the provided data. The table will be inserted
    at the third row of the first table in the document.

    Args:
        doc (docx.document.Document): The Document object where the table will be added.
        data (dict): A dictionary containing the data to populate the table.
            It should include a key 'TAB_RECAP' with a list of dictionaries.
    """

    print(f'[INFO] Nouveau dictionnaire : \n\n{data}')
    keys_first_element = list(data['NEW_TAB'][0].keys())

    container_table = doc.tables[0]
    table_test = container_table.rows[2].cells[1].add_table(
        rows = 1,
        cols = len(keys_first_element)
    )

    # Set table style
    table_test.style = 'Table Grid'

    headers = [
        'Méthode', 
        'Route', 
        'Paramètre', 
        'Profils concernés par cette fonctionnalité', 
        'Profils usurpant la fonctionnalité'
    ]

    for i, header in enumerate(headers):
        cell = table_test.cell(0, i)
        cell.text = header
        cell.paragraphs[0].runs[0].font.bold = True

    for recap in data['NEW_TAB']:
        new_row = table_test.add_row().cells
        for i, key in enumerate(keys_first_element):
            new_row[i].text = str(recap[key])

def create_report(template_path, data, placeholders, output_path):
    """
    Creates a report based on a template and provided data, and saves it to the specified output
    path.

    Args:
        template_path (str): The file path to the template document.
        data (dict): A dictionary containing data to replace placeholders and populate tables.
        placeholders (list): A list of placeholder keys to be replaced in the document.
        output_path (str): The file path where the generated report will be saved.

    Returns:
        str: The file path where the report was saved.
    """

    doc = Document(template_path)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for placeholder in placeholders:
                    if placeholder == 'TAB_RECAP':
                        if f'[{placeholder}]' in cell.text:
                            cell.paragraphs[0].clear()
                    elif placeholder == 'PROFILS':
                        if f'[{placeholder}]' in cell.text:
                            cell.text = cell.text.replace(f'[{placeholder}]', str(list_arg(data, 'PROFILS')))
                    elif placeholder == 'LISTE_ROUTES':
                        if f'[{placeholder}]' in cell.text:
                            cell.text = cell.text.replace(f'[{placeholder}]', str(list_arg(data, 'LISTE_ROUTES')))
                    else:
                        cell.text = cell.text.replace(f'[{placeholder}]', str(data[placeholder]))

    add_tables(doc, data)

    # Delete the CSV file if it exists
    if os.path.exists(output_path):
        print(f'[INFO] - Rapport existant supprimé : {output_path}')
        os.remove(output_path)

    doc.save(output_path)
    return output_path

def list_arg(data, arg):
    """
    Generates a formatted string from the elements of a list in the provided dictionary.

    Args:
        data (dict): The dictionary containing the data.
        arg (str): The key corresponding to the list of elements in the dictionary.

    Returns:
        str: A string with each element of the list preceded by a dash and followed 
             by a newline character.
    """

    args = ''
    for elem in data[arg]:
        args += f'- {elem} \n'

    return args
