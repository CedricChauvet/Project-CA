import fitz  # PyMuPDF
import pprint  # Pour un affichage plus lisible du dictionnaire

# Ouvrir le document PDF
doc = fitz.open("Tarifs BForBank2024 V8_WEB.pdf")


def read_a_page(doc, page_nb, reverse =False):
    # Sélectionner une page (par exemple, la première page)
    page = doc[page_nb]

    # Extraire le texte avec l'option "dict"
    text_dict = page.get_text("dict")
    # Afficher la structure générale du dictionnaire

    # Parcourir chaque bloc de texte
    font_sizes = set()

    block_inst= []
    for block in text_dict["blocks"]:
        
        if block["type"] == 0:  # Type 0 indique un bloc de texte
            block_text = ""
            bbox = block["bbox"]
            numberofelement=0
       

            # Extraire le texte et les tailles de police de chaque span    
            if bbox[3] < 800 and bbox[1] > 15:

                for line in block["lines"]:


                        for span in line["spans"]:
                        
                            
                            numberofelement += 1
                            block_text += (span["text"] + ", ")

                        font_sizes.add(span["size"])
                        size = span["size"]
                
                #print("\n", block_text,"#", numberofelement, "***", bbox)
                block_inst.append({"bbox": bbox, "text": block_text, "number" : numberofelement})
            
    print("font size", font_sizes)

    #print(block_inst[:])
    sorted_blocks = sorted(block_inst, key=lambda b: (b["bbox"][1], b["bbox"][0]))
    return sorted_blocks