"""
Deuxieme approche pour lecture de sommaire
By Ced+
Fonctionne avec
Tarifs CA_Acquitaine2024 V8_WEB.pdf
Tarifs BForBank2024 V8_WEB
"""


import fitz  # PyMuPDF
import pprint  # Pour un affichage plus lisible du dictionnaire
import pandas as pd


# doc = fitz.open("Tarifs CA_Acquitaine2024 V8_WEB.pdf")   ok
# doc = fitz.open("Tarifs BForBank2024 V8_WEB.pdf")    ok
# doc = fitz.open("Tarifs CA_AlpesProvence2024 V8_WEB.pdf")  ok
doc = fitz.open("Tarifs CA_Morbihan2024 V8_WEB.pdf")  # nope, double page


def read_a_page(doc, page_nb, reverse =False):
    """
    Sélectionner une page (par exemple, la première page)
    """

    page = doc[page_nb]
    return page

def extration_sommaire():
    """
    cherche le mot somaire dans le document
    return le numero de page
    """
    page_sommaire=[]
    #df = pd.DataFrame(columns=['Titre', 'ss-titre', 'page'])
    for page in doc:
        text_instances = page.search_for("SOMMAIRE")
        if text_instances != []:
            page_sommaire.append(page.number)
    if len(page_sommaire) == 0:
        print("nous n'avons pas trouvé de sommaire")
    if len(page_sommaire) > 1:
        print("Attention il y a plusieurs sommaires!") 
    return page_sommaire[0]

def affichage_page(page):
    """
    transforme une page en element exploitable
    """    
    text_dict = page.get_text("dict")
    # Création d'un dictionnaire contenant tout ce qu'il y a d'utile
    block_inst= []
    
    for block_nbr, block in enumerate(text_dict["blocks"]):       
        if block["type"] == 0:  # Type 0 indique un bloc de texte
            block_text = ""
            bbox = block["bbox"]
            numberofelement=0
       
            # Extraire le texte et les tailles de police de chaque span    
            for line in block["lines"]:
                    for span in line["spans"]:
                        numberofelement += 1
                        # on enleve les pages, les numero de titre,
                        if not span["text"][-1].isdigit(): # on considere que si ca termine par un chiffre, ce n'est pas essentiel
                            block_text += (span["text"] + "\n")
                    
                    size = span["size"]
            # liste d'elements. Modifiable si souhaité
            block_inst.append({"bbox": bbox, "text": block_text, "number" : numberofelement, "font":size, "line": block_nbr})
    return block_inst


def nettoyage_page(blocks):
    """
    permet d'effacer des element non desirés
    """
    
    number =[]
    for bloc in blocks:
        # enleve le bloc sommaire, attention pose un bug sur le premier element, laisser commenté
        #if bloc["text"].count("SOMMAIRE"):
        #    number.append(bloc["line"])
        
        # enleve tout ce qui est trop petit ou trop long
        if bloc["font"] < 7 or len(bloc["text"])>400:
            number.append(bloc["line"])
        
        # enleve les en tetes  800 est en haut et 15 est en bas de la page
        if bloc["bbox"][3] > 800 or bloc["bbox"][1] < 15:
            number.append(bloc["line"])
    
    number= sorted(number, reverse=True)
    for n in number:
        del blocks[n]
    return blocks


def sommaire_pandas(page_sommaire):
    """
    prend les elements selectionés en table pandas
    """
    page = read_a_page(doc, page_sommaire)
    blocks = affichage_page(page)
    blocks = nettoyage_page(blocks)
    
    # page suivant celle du sommaire
    page2 = read_a_page(doc, page_sommaire + 1)
    blocks2 = affichage_page(page2)
    blocks2 = nettoyage_page(blocks2)
    

    # # teste si la page suivante fait partie du sommaire
    if blocks[0]["text"].find(blocks2[0]["text"][0:-1]) == -1:
        print("plusieur page de sommaire")
        blocks = blocks + blocks2
    
    size = set()
    
    # recupere les size de la selection blocks
    for bloc in blocks:
        # peut etre rajouter un instruction pour ne pas selectoinner  la taille de font du sommaire
        size.add(bloc["font"])
    size = list(size)

    sorted(size)
    print("size", size, "idealement de taille 2")

    df = pd.DataFrame(columns=['Titre', 'ss-titre'])
    
    for bloc in blocks:
        if bloc["font"] == max(size):
            title= bloc["text"].split("\n")[0]
            df.loc[len(df)] = [title, " "]

        if bloc["font"] == size[-2]:
            for i in bloc["text"].split("\n")[0:-1]:
                df.loc[len(df)] = [title, i]
    print(df)
    


sommaire = extration_sommaire()
sommaire_pandas(sommaire)



# affiche le texte sur le terminal, et les options
page = read_a_page(doc, sommaire)
blocks = affichage_page(page)
blocks = nettoyage_page(blocks)
#for bloc in blocks:
   # print(bloc["text"], bloc["font"])#, "n", bloc["line"],  bloc["bbox"][1], bloc["bbox"][3])
   


