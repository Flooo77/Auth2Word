"""
auth2word.py

This script integrates XML parsing, placeholder extraction, and Word document manipulation 
to generate reports based on XML data and a Word template. It also includes CSV handling 
to allow user input for specific data points.

Workflow:
1. Parses an XML file to extract data.
2. Extracts placeholders from a Word document template.
3. Initializes a CSV file with extracted data for user input.
4. Waits for user to complete the CSV file.
5. Processes the completed CSV file to update data.
6. Replaces placeholders in the Word template with data from the XML and CSV.
7. Adds data tables to the Word document based on XML data.
8. Saves the final report to a specified file.

Modules used:
- parser: For parsing XML files and extracting data.
- placeholder: For extracting placeholders from a Word document template.
- create: For handling Word documents, including placeholder replacement and table addition.
- csv_handler: For initializing and processing CSV files for user input.

Functions:
- main: Orchestrates the process of parsing XML, extracting placeholders, initializing CSV, 
        waiting for user input, processing the CSV, and generating the Word report.

Example usage:
    XML_FILE_PATH = "Auth_Analyzer_Report.xml"
    TEMPLATE_PATH = "auth_template.docx"
    OUTPUT_PATH = "rapport_final.docx"
    CSV_PATH = "template.csv"
    main(XML_FILE_PATH, TEMPLATE_PATH, OUTPUT_PATH, CSV_PATH)
"""

from modules.create import create_report
from modules.parser import parse_xml
from modules.placeholder import get_placeholders
from modules.csv_handler import initialize_csv, read_csv, process_csv

def main(xml_file_path, template_path, output_path, csv_path):
    """
    Main function to generate a Word report based on XML data and a Word template.
    Args:
        xml_file_path (str): The path to the XML file containing the data.
        template_path (str): The path to the Word template document.
        output_path (str): The path where the generated Word report will be saved.
        csv_path (str): The path to the CSV file for user input.
    """
    # Extract placeholders from the Word template
    placeholders = get_placeholders(template_path)

    # Parse the XML file to extract data
    data = parse_xml(xml_file_path)

    # Initialize the CSV file with the recap data
    initialize_csv(data, csv_path)

    # Wait for user to complete the CSV file
    input ("The Auth_Analyser_Report.csv has been created, please fill it.")
    completed = input("Have you completed the CSV file? (y/n): ")
    while completed.lower() != 'y':
        completed = input("Please complete the CSV file and enter 'y' when done: ")

    # Read the completed CSV file
    csv_data = read_csv(csv_path)

    # Process the completed CSV file to update data
    process_csv(data, csv_data)

    # Create the Word report by replacing placeholders and adding data tables
    create_report(template_path, data, placeholders, output_path)

    print(f"Report generated and saved to: {output_path}")

# Example usage (if running this script directly)
if __name__ == "__main__":
    # Define file paths
    XML_FILE_PATH = "Auth_Analyzer_Report.xml"
    TEMPLATE_PATH = "auth_template.docx"
    OUTPUT_PATH = "rapport_final.docx"
    CSV_PATH = "template.csv"

    # Generate the report
    main(XML_FILE_PATH, TEMPLATE_PATH, OUTPUT_PATH, CSV_PATH)
