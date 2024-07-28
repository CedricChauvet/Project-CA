
import fitz  # PyMuPDF
import pprint  # Pour un affichage plus lisible du dictionnaire
import pandas as pd


read_a_page = __import__('pymu_01').read_a_page

def number_selected_blocks(blocks):
    print("nb de blocks", len(blocks))

# afine la selection des blocks selon un interval vertical y1, y2
def aera_selecting(blocks, y1, y2):

    for i in blocks:
        if not( i["bbox"][1] > y1 and i["bbox"][3] < y2):
            blocks.remove(i)

    return blocks

def font_page():
    
    # Parcourir chaque bloc de texte
    font_sizes = set()



def search_word(word):
    """
    not working yet
    """

    resultats = []
    num_page = None
    for num_page in range(len(doc)):
        if num_page > 3:
            page = doc[num_page]
            occurrences = page.search_for(word)

            return num_page
    
    

def extration_sommaire():
    page_sommaire=[]
    df = pd.DataFrame(columns=['Titre', 'ss-titre', 'page'])
    for page in doc:
        text_instances = page.search_for("SOMMAIRE")
        if text_instances != []:
            page_sommaire.append(page.number)
            print(text_instances, page.number)  # on voit qu'il y a 2 sommaires dans le document

    blocks, font_size = read_a_page(doc, page_sommaire[0])
    for block in blocks:
        strat_json = False
        #print(block["text"], block["font"])
        if block["text"][0:8].upper() == "SOMMAIRE":
            start_json =True
            is_empty = False
        if start_json == True:
            if block["font"] == font_size[-1]:
                if is_empty == True:
                    df.loc[len(df)] = [title, "vide", 0]
                title= block["text"]
                is_empty = True

            if block["font"] == font_size[-2]:
                sous_title = block["text"]
                for i in block["text"].split("\n")[0:-1]:
                    df.loc[len(df)] = [title, i, 0]
                is_empty = False
    
    df.loc[len(df)] = [title, "vide", 0]             
    print(df)







doc = fitz.open("Tarifs BForBank2024 V8_WEB.pdf")
blocks, font_size = read_a_page(doc, 2)
print("font",font_size)
aera_blocks = aera_selecting(blocks, 0, 100)
number_selected_blocks(aera_blocks)

extration_sommaire()