import fitz  # PyMuPDF

# Ouvrir le document PDF
doc = fitz.open("Tarifs BForBank2024 V8_WEB.pdf")

# Sélectionner une page (par exemple, la première page)
page = doc[0]

# Extraire le texte avec l'option "dict"
text_dict = page.get_text("dict")

# Créer une liste pour stocker les blocs de texte
blocks = []

# Parcourir chaque bloc de texte
for block in text_dict["blocks"]:
    if block["type"] == 0:  # Type 0 indique un bloc de texte
        for line in block["lines"]:
            for span in line["spans"]:
                # Ajouter les informations pertinentes à la liste
                blocks.append({
                    "bbox": block["bbox"],
                    "text": span["text"],
                    "block_no": block["number"],
                    "size": span["size"],
                    "font": span["font"]
                })

# Trier les blocs de texte de haut en bas puis de gauche à droite
sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))

# Parcourir chaque bloc de texte trié et afficher les informations
for block in sorted_blocks:
    print(f"Bloc {block['block_no']} :")
    print(f"  Coordonnées : {block['bbox']}")
    print(f"  Texte : {block['text']}")
    print(f"  Taille de police : {block['size']}")
    print(f"  Police : {block['font']}")

# Fermer le document
doc.close()