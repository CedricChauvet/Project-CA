import os
import fitz
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout, TimeDistributed
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# Chargement du CSV
def load_csv(file_path):
    df = pd.read_csv(file_path, sep=";", encoding="latin-1" , engine='python')
    if len(df.columns) == 1:
        df = pd.read_csv(file_path, sep=';')
    return df



# Chargement et préparation des données
pdf_texts = []
summaries = []

pdf_file = os.path.join('./Data_train/pdf/', 'Tarifs BForBank2024 V8_WEB.pdf')
csv_file = os.path.join('./Data_train/csv/', 'Tarifs_BForBank2024_sommaire.csv')


csv_data = load_csv(csv_file)
# print(csv_data)


text_pdf = extract_text_from_pdf(pdf_file)
#print(text_pdf)


# Préparation des sommaires
summaries = []
for _, row in csv_data.iterrows():
    title = row.iloc[0]  # Titre principal (première cellule de chaque ligne)
    subtitles = [subtitle for subtitle in row.iloc[1:] if isinstance(subtitle, str) and pd.notna(subtitle)]
    summary = f"{title}\n" + "\n".join(subtitles)
    summaries.append(summary)

# Tokenisation
tokenizer = Tokenizer()
tokenizer.fit_on_texts([text_pdf] + summaries)

X = tokenizer.texts_to_sequences([text_pdf] * len(summaries))
y = tokenizer.texts_to_sequences(summaries)

# Padding
max_len = max(len(seq) for seq in X + y)
X = pad_sequences(X, maxlen=max_len, padding='post')
y = pad_sequences(y, maxlen=max_len, padding='post')

# Conversion de y en format one-hot
vocab_size = len(tokenizer.word_index) + 1
y = np.array([np.eye(vocab_size)[sequence] for sequence in y])

# Création du modèle LSTM
embedding_dim = 100
lstm_units = 128

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(LSTM(lstm_units, return_sequences=True))
model.add(LSTM(lstm_units, return_sequences=True))
model.add(TimeDistributed(Dense(vocab_size, activation='softmax')))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entraînement du modèle
model.fit(X, y, epochs=10, batch_size=1, verbose=1)


# Fonction pour générer un sommaire
def generate_summary(text):
    seq = tokenizer.texts_to_sequences([text])
    padded_seq = pad_sequences(seq, maxlen=max_len)
    pred = model.predict(padded_seq)
    
    pred_text = []
    for word_index in pred[0]:
        word = tokenizer.index_word.get(int(np.argmax(word_index)), "")
        if word:
            pred_text.append(word)
    
    # Formatage du sommaire prédit
    pred_title = pred_text[0]  # Premier mot comme titre
    pred_subtitles = pred_text[1:]  # Reste comme sous-titres
    
    formatted_summary = f"{pred_title}\n" + "\n".join(pred_subtitles)
    return formatted_summary

# Génération d'un sommaire pour le PDF d'origine


print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
generated_summary = generate_summary(text_pdf)
print("Sommaire généré :")
print(generated_summary)

print("\nExemples de sommaires originaux :")
for i, summary in enumerate(summaries[:3]):  # Affiche les 3 premiers sommaires
    print(f"\nSommaire {i+1}:")
    print(summary)