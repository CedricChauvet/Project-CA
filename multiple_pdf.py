"""
Deuxieme approche pour lecture de sommaire avec lecture de plusieurs pdf
By Ced+
"""


import fitz  # PyMuPDF
import pprint  # Pour un affichage plus lisible du dictionnaire
import pandas as pd
import os


sommaire_pandas = __import__('pymu_12').sommaire_pandas
extration_sommaire = __import__('pymu_12').extration_sommaire


from pathlib import Path

# Spécifiez le chemin du répertoire
repertoire = Path('./PDF')

# Liste tous les fichiers dans le répertoire
fichiers = [f for f in repertoire.iterdir() if f.is_file()]
print("len", len(fichiers))
# Liste des fichiers PDF à ouvrir
pdf_files = ['document1.pdf', 'document2.pdf', 'document3.pdf']

# Ouvrir et traiter chaque document PDF
documents = []
path_csv = "./my_csv2/"
for file in fichiers[0:15]:
        doc = fitz.open(file)
        documents.append(doc)
        #print(f"Ouvert: {file}")

    # Effectuer des opérations sur les documents ouverts
for doc in documents:
        sommaire = extration_sommaire(doc)
        try: 
            sommaire_pandas(sommaire, doc)
            
            df, good = sommaire_pandas(sommaire,doc)
            # print(df)
            
        except:
            print("An exception occurred\n\n")
        df.to_csv(path_csv + file.name[:-4] + '.csv', index=False)
        # print(f"Nombre de pages dans {doc.name}: {doc.page_count}")

# for doc in documents:
#         doc.close()
#         print(f"Fermé: {doc.name}")



# documents = []
# # Crée une variable string pour chaque fichier et affiche son nom
# for fichier in fichiers[0:20]:
#     # Convertit l'objet Path en chaîne de caractères
#     name_pdf = fichier.name
#     print("namefile", name_pdf)
#     # dossier ou l'on recupere les sommaire extraits
#     

#     doc = fitz.open(name_pdf)
#     documents.append(doc)








#    doc = fitz.open(name_pdf)
#    doc.close()
    # sommaire = extration_sommaire(doc)

    # # return the dataframe, good if the file looks like ok
    # df, good = sommaire_pandas(sommaire,doc)

    # df.to_csv(path_csv + name_pdf[:-4] + '.csv', index=False)
