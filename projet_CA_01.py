"""
Programme permettant de selectionner les titres dans un document pdf
contient de nouvelles classes pour servir au projet

by Ced 
"""

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextBoxHorizontal, LTChar, LTTextLineHorizontal


class Document():
    """
    superclasse
    """

    def __init__(self,file_path):
        self.file_path = file_path
        self.pages = self.read_doc()
        self.nb                         # nombre de pages du document
    
    
    def __len__(self):
        
        return len(self.pages)

    def read_doc(self):
        """
        extrait un document pdf
        renvoie une liste des pages du document, de type " LTPage"
        """
        extraction =  extract_pages(self.file_path)
        pag=[]
        for page in extraction:
            pag.append(Page(page,page.pageid))
        
        self.nb = len(pag)
        return pag




class Page(Document):
    """
    class page
    """

    def __init__(self, page, id, ):
        self.page=page
        self.id=id
        self.elements = self.get_element()

    def number_lines(self):
        liste1=set()
        for i in self.page:
            liste1.add(i.x0)

    # on peux ajouter des choses comme bbox ici    
    def get_element(self):
        elements=[]
        for elt in self.page:
            if isinstance(elt, LTTextContainer):
               for text_line in elt:
                    if isinstance(text_line,LTTextLineHorizontal):         # un poil compilqué mais il faut rentrer dedans pour 
                        taille_line = next(iter(text_line)).size           # rentrer dans les details, voir bbox et font
                        # print(dir(LTTextLineHorizontal))                 # peut servir            
                        elements.append(Element(text_line, taille_line))
        return elements
 


class Element(LTTextLineHorizontal):
    """
    l'element LTTextLineHorizontal est ce qui se rapproce le plus du texte présent dans le pdf
    """
    def __init__(self, elt, size):
        
        self.elt = elt
        self.x0 = self.X_pos
        self.y0 = self.Y_pos
        self.size = size

    # est utiliser pour organiser et trier les textes
    def __lt__(self, other):
        if self.Y_pos > other.Y_pos:
            return True
        elif self.Y_pos == other.Y_pos:
            return self.X_pos < other.X_pos
        else:
            return False
    
    # print()
    def __repr__(self):
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        if self.size > 12:
            color = OKBLUE
        else: 
            color =  OKGREEN
        return color + self.elt.get_text()

    @property
    def X_pos(self):
        """
        retourne  la valeur x0 qui est la limite gauche de la boxe
        """
        return self.elt.x0
    @property
    def Y_pos(self):
        """
        retourne  la valeur x0 qui est la limite basse de la boxe
        """
        return self.elt.y0



# ouverture du fichier
Docu = Document('Tarifs CA_Corse2024 V8_WEB.pdf')

#extraction des pages
pagesss= Docu.read_doc()

# selection d'elements d'une page
# eltms= pagesss[3].elements

# lecture du codument entier
for page in pagesss[:]:
    page_triee = sorted(page.elements[:])
    print(page_triee)


