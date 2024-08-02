"""
This module provides functions for parsing XML files and extracting relevant data 
into a structured format.

Functions:
- initialize_data: Initializes and returns a dictionary with default values for 
                   report data.
- get_first_message: Retrieves the first 'Message' element from the XML root.
- extract_profiles: Extracts profile names from the first 'Message' element and 
                    adds them to the data dictionary.
- extract_app_name: Extracts the application name from the first 'Message' element
                    and updates the data dictionary.
- extract_recap_entries: Extracts recap entries from all 'Message' elements in the
                         XML root and updates the data dictionary.
- extract_method: Extracts the HTTP method from a 'Message' element and adds it to
                  the recap entry.
- extract_path_and_params: Extracts the path and query parameters from a 'Message'
                           element and updates the recap entry and data.
- extract_bypass_statuses: Extracts bypass statuses for each profile from a 'Message' 
                           element and adds them to the recap entry.
- parse_xml: Parses an XML file, extracts data, and returns it in a structured format.
"""

import xml.etree.ElementTree as ET


def initialize_data():
    """
    Initializes and returns a dictionary with default values for the report data.

    Returns:
        dict: A dictionary with keys 'PROFILS', 'NOM_APP', 'TAB_RECAP', 'PRIVILEGE', 
              'PROBLEME', and 'LISTE_ROUTES', initialized with default values.
    """

    return {
        'PROFILS': [],
        'NOM_APP': '',
        'TAB_RECAP': [],
        'PRIVILEGE': '',
        'PROBLEME' : ', des problèmes de cloisonnement verticaux ont été observés. En d\'autres termes cela signifie que les données entre différents niveaux d\'accès ne sont pas correctement isolées. Cela peut entraîner des fuites de données sensibles entre les utilisateurs ayant des privilèges différents.',
        'LISTE_ROUTES': [],
    }

def get_first_message(root):
    """
    Retrieves the first 'Message' element from the XML root.

    Args:
        root (xml.etree.ElementTree.Element): The root element of the XML tree.

    Returns:
        xml.etree.ElementTree.Element: The first 'Message' element, or None if it 
        does not exist.
    """

    return root.find('Message')

def extract_profiles(first_message, data):
    """
    Extracts profile names from the 'first_message' element and adds them to the 
    'data' dictionary.

    Args:
        first_message (xml.etree.ElementTree.Element): The 'Message' element from
        which to extract profile names.
        data (dict): The dictionary to which extracted profiles will be added.
    """

    for elem in first_message:
        if 'Bypass_Status' in elem.tag:
            profile = elem.tag.split('_Bypass_Status')[0]
            data['PROFILS'].append(profile)

def extract_app_name(first_message, data):
    """
    Extracts the application name from the 'first_message' element and updates the
    'data' dictionary.

    Args:
        first_message (xml.etree.ElementTree.Element): The 'Message' element from
        which to extract the application name.
        data (dict): The dictionary to which the application name will be added.
    """

    host = first_message.find('Host')
    if host is not None:
        data['NOM_APP'] = host.text

def extract_recap_entries(root, data):
    """
    Extracts recap entries from all 'Message' elements in the XML root and updates 
    the 'data' dictionary.

    Args:
        root (xml.etree.ElementTree.Element): The root element of the XML tree 
        containing 'Message' elements.
        data (dict): The dictionary to which recap entries will be added.
    """

    for message in root.findall('Message'):
        recap_entry = {}
        extract_method(message, recap_entry)
        extract_path_and_params(message, recap_entry, data)
        extract_bypass_statuses(message, recap_entry, data)
        data['TAB_RECAP'].append(recap_entry)

def extract_method(message, recap_entry):
    """
    Extracts the HTTP method from a 'Message' element and adds it to the recap entry.

    Args:
        message (xml.etree.ElementTree.Element): The 'Message' element from which 
        to extract the HTTP method.
        recap_entry (dict): The dictionary to which the HTTP method will be added.
    """

    method = message.find('Method')
    recap_entry['method'] = method.text if method is not None else ''

def extract_path_and_params(message, recap_entry, data):
    """
    Extracts the path and query parameters from a 'Message' element and updates the 
    recap entry and data.

    Args:
        message (xml.etree.ElementTree.Element): The 'Message' element from which to
        extract the path and parameters.
        recap_entry (dict): The dictionary to which the path and parameters will be 
        added.
        data (dict): The dictionary to which the route will be added.
    """

    path = message.find('Path')
    if path is not None:
        full_path = path.text
        if '?' in full_path:
            route, param = full_path.split('?', 1)
        else:
            route, param = full_path, ''
        recap_entry['route'] = route
        recap_entry['param'] = param
        data['LISTE_ROUTES'].append(route)
    else:
        recap_entry['route'] = ''
        recap_entry['param'] = ''

def extract_bypass_statuses(message, recap_entry, data):
    """
    Extracts bypass statuses for each profile from a 'Message' element and adds them
    to the recap entry.

    Args:
        message (xml.etree.ElementTree.Element): The 'Message' element from which to 
        extract bypass statuses.
        recap_entry (dict): The dictionary to which the bypass statuses will be added.
        data (dict): The dictionary containing the list of profiles.
    """

    for profile in data['PROFILS']:
        bypass_status = message.find(f'{profile}_Bypass_Status')
        recap_entry[profile] = bypass_status.text if bypass_status is not None else ''

def parse_xml(file_path):
    """
    Parses an XML file and extracts relevant data into a dictionary.

    Args:
        file_path (str): The path to the XML file to be parsed.

    Returns:
        dict: A dictionary containing the extracted data from the XML file.
    """

    tree = ET.parse(file_path)
    root = tree.getroot()

    data = initialize_data()
    first_message = get_first_message(root)

    if first_message is not None:
        extract_profiles(first_message, data)
        extract_app_name(first_message, data)

    extract_recap_entries(root, data)

    return data
