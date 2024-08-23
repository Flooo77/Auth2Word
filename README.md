# Rapport de Vulnérabilité pour les Défauts de Contrôle d'Accès

Ce projet permet de générer un rapport de vulnérabilité à partir d'un fichier XML exporté par Auth Analyzer (extension Burp Suite). Le rapport est généré sous forme de document Word en utilisant un modèle prédéfini.

## Structure du Projet
```
.
├── Auth_Analyzer_Report.xml
├── README.md
├── acces_routes.csv
├── auth2word.py
├── auth_template.docx
├── modules
│   ├── create.py
│   ├── csv_handler.py
│   ├── parser.py
│   └── placeholder.py
└── rapport_final.docx
```

## Installation

Pour utiliser ce script, Il est nécessaire d'avoir Python et les bibliothèques nécessaires installées. Installer les bibliothèques requises en utilisant pip :
```
pip install python-docx
```

Cloner ce répertoire :
```
git clone https://github.com/Flooo77/Auth2Word.git
```

## Utilisation 
Au préalable exporter le rapport de Auth Analyser au format XML.

Se placer dans le répertoire du projet, exécuter le script `auth2word.py` en fournissant le chemin du fichier XML.
```
python auth2word.py chemin/vers/fichier/XML.xml
```

## Fonctionnement

Ce script Python utilise les données extraites d'un fichier XML généré par Auth Analyzer pour générer un rapport de vulnérabilité au format Word. Voici comment il fonctionne :

1. **Extraction des données XML** :
   - Le script commence par analyser le fichier XML spécifié en ligne de commande à l'aide de la fonction parse_xml du module parser.py. Ce module extrait les informations pertinentes comme les profils d'accès, les chemins d'accès avec leurs paramètres, et détermine le compte ayant le plus de privilèges.

2. **Fitlrage des doublons** :
   - Lors de l'extraction des chemins d'accès et de leurs paramètres, le script vérifie s'il existe des doublons dans les routes extraites. Seules les routes uniques sont conservées, ce qui permet d'éviter la redondance dans les données.

3. **Extraction des placeholders** :
   - Il charge ensuite le modèle Word défini par le chemin auth_template.docx à l'aide de la fonction get_placeholders du module placeholder.py. Cette fonction identifie et récupère tous les placeholders utilisés dans le modèle.

4. **Initialisation du fichier CSV** :
   - Un fichier CSV (acces_routes.csv) est initialisé avec les données extraites du XML à l'aide de la fonction initialize_csv du module csv_handler.py. L'utilisateur doit remplir ce fichier avec les informations complémentaires nécessaires.

5. **Attente de l'utilisateur** :
   - Le script attend que l'utilisateur complète le fichier CSV avec les données manquantes. Une fois le fichier complété, l'utilisateur confirme la complétion.

6. **Traitement du fichier CSV complété** :
   - Les données du fichier CSV complété sont lues et traitées à l'aide de la fonction process_csv du module csv_handler.py, ce qui met à jour les données avec les informations fournies par l'utilisateur.

7. **Remplacement des placeholders et ajout des tables** :
   - Les placeholders trouvés dans le modèle Word sont remplacés par les données extraites du fichier XML et complétées par celles du CSV à l'aide de la fonction create_report du module create.py. Les données spécifiques incluent les chemins d'accès, les paramètres, les méthodes d'accès, ainsi que la liste des routes analysées.

8. **Génération du rapport final** :
   - Le rapport final est généré sous le nom rapport_final.docx dans le répertoire de travail. Ce document contient un tableau récapitulatif des chemins d'accès, leurs paramètres et méthodes, ainsi qu'une liste des routes analysées.

9. **Affichage du résultat** :
   - Une fois le rapport généré avec succès, un message confirmant la réussite de l'opération est affiché dans la console.
