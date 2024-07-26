
import fitz  # PyMuPDF
import pprint  # Pour un affichage plus lisible du dictionnaire

read_a_page = __import__('pymu_01').read_a_page

def number_selected_blocks(blocks):
    print("nb de blocks", len(blocks))

# afine la selection des blocks selon un interval vertical y1, y2
def aera_selecting(blocks, y1, y2):

    for i in blocks:
        if not( i["bbox"][1] > y1 and i["bbox"][3] < y2):
            blocks.remove(i)

    return blocks

def extration_sommaire():
    page_sommaire=[]
    for page in doc:
        text_instances = page.search_for("SOMMAIRE")
        if text_instances != []:
            page_sommaire.append(page.number)
            print(text_instances, page.number)  # on voit qu'il y a 2 sommaires dans le document
    print(page_sommaire)

doc = fitz.open("Tarifs BForBank2024 V8_WEB.pdf")
blocks = read_a_page(doc, 2)

aera_blocks = aera_selecting(blocks, 0, 100)
number_selected_blocks(aera_blocks)

extration_sommaire()