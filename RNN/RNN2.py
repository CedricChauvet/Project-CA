import os
import pandas as pd
import fitz  # PyMuPDF
#from tensorflow.keras.preprocessing.text import Tokenizer
#from tensorflow.keras.preprocessing.sequence import pad_sequences
#from sklearn.model_selection import train_test_split

# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Dossiers contenant les PDF et CSV
pdf_folder = '.\Data_train\pdf'
csv_folder = '.\Data_train\csv'

# Listes pour stocker les données
texts = []
summaries = []


# ajout manuel des fichiers traités
fichier1 = "Tarifs_BForBank2024_sommaire"
fichier2 = "Tarifs CA_Acquitaine2024 V8_WEB"
# Traitement des PDF et CSV
pdf_path = os.path.join(pdf_folder, 'Tarifs BForBank2024 V8_WEB.pdf')
csv_path = os.path.join(csv_folder, 'Tarifs_BForBank2024_sommaire.csv')

# Extraction du texte du PDF
if os.path.exists(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    texts.append(text)
else:
    print(f"PDF non trouvé : {pdf_path}")


# Chargement du sommaire depuis le CSV
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path, encoding='latin-1')
    if 'summary' in df.columns:
        summary = df['summary'].iloc[0]  # Supposons que le sommaire est dans la première ligne
        summaries.append(summary)
    else:
        print(f"Colonne 'summary' non trouvée dans {csv_path}")
    
else:
    print(f"CSV non trouvé : {csv_path}")
    
exit()

# Vérification que nous avons le même nombre de textes et de sommaires
assert len(texts) == len(summaries), "Le nombre de textes et de sommaires ne correspond pas"

# Tokenisation
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts + summaries)
vocab_size = len(tokenizer.word_index) + 1

# Conversion des textes et sommaires en séquences
X = tokenizer.texts_to_sequences(texts)
y = tokenizer.texts_to_sequences(summaries)

# Padding
max_length = 500  # Ajustez selon vos besoins
X = pad_sequences(X, maxlen=max_length)
y = pad_sequences(y, maxlen=max_length)

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Forme des données d'entraînement:", X_train.shape)
print("Forme des données de test:", X_test.shape)

# Ces données (X_train, X_test, y_train, y_test) sont maintenant prêtes à être utilisées pour l'entraînement du modèle