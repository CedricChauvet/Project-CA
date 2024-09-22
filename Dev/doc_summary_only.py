"""
extraction des pages de sommaire et de litige
pourquoi?
En regle generale, le sommaire est le premier element du sommaire
Le litige est souvent le dernier element du sommaire
permet de determiner si le sommaire est sur 1 ou 2 pages

Enregistre les sommaire dans le repertoire sommaires
"""
import fitz  # PyMuPDF
import os # for file handling


# assign directory
directory = '../PDF_CGV' # directory containing the PDF files
try:
    os.makedirs("sommaires") # create a directory to save the summaries
except:
    print("Erreur: Le dossier 'sommaires' existe deja")

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f) # print the file name

    doc = fitz.open(f)
    page_sommaire=[]
    page_litige=[]

    for num_page in range(len(doc)):
        page = doc[num_page]
        if page.search_for("sommaire") != []:
            page_sommaire.append(num_page)
        if page.search_for("litige") != []:
            page_litige.append(num_page)
        else:
            continue
            
    #  phase 2 enregistrer le sommaire dans un nouveau fichier
    
    try:
        new_pdf = fitz.open()
        new_pdf.insert_pdf(doc, from_page=page_sommaire[0], to_page=page_litige[0])
        f_sum = os.path.join("sommaires", "sum_" + filename)
        new_pdf.save( f_sum  )

        #print("page_sommaire", page_sommaire[0])   
        #print("page_litige", page_litige[0])
        doc.close()

    except:
        print("Erreur", filename)
    # pour le cas de la picardie, bug du a l'absence du mot sommaire dans le document
