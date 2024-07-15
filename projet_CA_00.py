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
        self.size = self.get_size()
    def number_lines(self):
        liste1=set()
        for i in self.page:
            liste1.add(i.x0)

        
    def get_element(self):
        elements=[]
        for elt in self.page:
            if isinstance(elt, LTTextContainer) :
               elements.append(Element(elt))
        return elements

    def get_size(self):
        # methode pour obtenir size_car
        elt_text = next(iter(elt))   # objet de type  LTTextLineHorizontal
        elt_size = next(iter(elt_text)).size   # cet objet a une size (premier caractere :)
        return elt_size.size    


class Element(Page):

    def __init__(self, elt):
        
        self.elt = elt
        self.x0 = self.X_pos
        self.y0 = self.Y_pos
        # self.color = self.get_color()
        

        if not isinstance(self.elt, LTTextContainer):
            raise("Element must be a text")


    def __repr__(self):
        return self.elt.get_text()
        # return self.color + self.elt.get_text()
    
    def __lt__(self, other):
        if self.Y_pos > other.Y_pos:
            return True
        elif self.Y_pos == other.Y_pos:
            return self.X_pos < other.X_pos
        else:
            return False
    
    # def get_color(self):
    #    if isinstance(self, LTTextLineHorizontal):
    #        return '\033[1m'  # bleu
    #    else:
    #        return '\033[92m' #vert
    

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
Docu = Document('Tarifs BForBank2024 V8_WEB.pdf')

#extraction des pages
pagesss= Docu.read_doc()

# selection d'elements d'une page
eltms= pagesss[3].elements

# affichage des textes de chaque elment
#print(eltms[:])
#print("plus ou moins", eltms[5]> eltms[0])
eltms_tries = sorted(eltms)

#for page in pagesss:
#    page_triee = sorted(page.elements[:])
  #  print(page_triee)


print(dir(LTTextLineHorizontal))