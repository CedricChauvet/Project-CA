"""
utilisé pour faire un tableau des banques present dans les pdf
"""
import os  # for file handling
import csv  # for writing CSV

# assign directory
directory = '../PDF_CGV'  # directory containing the PDF files

# Création et écriture dans le fichier CSV
with open('personnes.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Écrire l'en-tête du CSV
    writer.writerow(['Nom du fichier', 'Taille (en octets)', 'Chemin complet'])
    
    # Parcourir les fichiers dans le répertoire
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):  # On ne prend que les fichiers PDF
            file_path = os.path.join(directory, filename)  # Chemin complet du fichier
            file_size = os.path.getsize(file_path)  # Taille du fichier
            
            # Écrire une ligne dans le CSV avec le nom, la taille et le chemin
            writer.writerow([filename[7:-4]])
        
            print(f"Fichier {filename} ajouté au CSV.")

    print("Fichier CSV créé avec succès !")