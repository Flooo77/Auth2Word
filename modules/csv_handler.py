"""
csv_handler.py

This module provides functionality for initializing and processing CSV files to 
facilitate user input for specific data points that are not available in the XML
file. It primarily supports the workflow of the auth2word script.

Functions:
- initialize_csv: Creates a CSV file with headers based on extracted XML data and
                  profile names, and initializes it with empty fields for user input.
- process_csv: Reads the completed CSV file and updates the data dictionary with 
               user-provided information.

Example usage:
    data = parse_xml("Auth_Analyzer_Report.xml")
    csv_path = "template.csv"
    initialize_csv(data, csv_path)
    # User completes the CSV file
    process_csv(data, csv_path)
"""

import csv
import os

def initialize_csv(data, csv_path):
    """
    Initializes a CSV file with headers based on the recap data and profile names.
    Args:
        data (dict): The dictionary containing extracted data from the XML.
        csv_path (str): The path to the CSV file to be created.
    """
    headers = list(data['TAB_RECAP'][0].keys())

    # Delete the CSV file if it exists
    if os.path.exists(csv_path):
        print(f'\n\n[INFO] - Fichier CSV existant supprimé : {csv_path}\n')
        os.remove(csv_path)

    with open(csv_path, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for entry in data['TAB_RECAP']:
            row = [
                    entry['method'],
                    entry['route'],
                    entry['param']
                  ] + ['' for _ in data['PROFILS']]

            writer.writerow(row)

def read_csv(csv_path):
    """Reads the CSV file and returns its content as a list of dictionaries.

    Args:
        csv_path (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries representing the rows in the CSV file.
    """
    with open(csv_path, mode='r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        csv_data = [row for row in reader]
    return csv_data

def process_csv(data, csv_data):
    """
    Processes the completed CSV file and updates the data dictionary.
    Args:
        data (dict): The dictionary containing extracted data from the XML.
        csv_data (list): The list of rows from the completed CSV file.
    """

    data['NEW_TAB'] = []

    for row in csv_data:
        profils_concernes = []
        profils_usurpes = []

        # Trouver l'entrée correspondante dans TAB_RECAP
        matching_entry = None
        for entry in data['TAB_RECAP']:
            if entry['method'] == row['method'] and entry['route'] == row['route'] and entry['param'] == row['param']:
                matching_entry = entry
                break

        if not matching_entry:
            continue  # Skip if no matching entry is found

        # Comparaison des statuts et des valeurs du csv
        for profile in data['PROFILS']:
            csv_status = row[profile].strip().lower()
            xml_status = matching_entry.get(profile, '').strip().lower()

            if xml_status == 'different':
                if csv_status == 'x':
                    profils_concernes.append(profile)
            elif xml_status in ['same', 'similar']:
                if csv_status == 'x':
                    profils_concernes.append(profile)
                else:
                    profils_usurpes.append(profile)

        # Mise à jour de NEW_TAB avec method, route, param, profils_concernes et profils_usurpes
        # Ajouter l'entrée seulement si profils_usurpes n'est pas vide
        if profils_usurpes:
            new_entry = {
                'method': matching_entry['method'],
                'route': matching_entry['route'],
                'param': matching_entry['param'],
                'profils_concernes': ', '.join(profils_concernes),
                'profils_usurpes': ', '.join(profils_usurpes)
            }

            data['NEW_TAB'].append(new_entry)
