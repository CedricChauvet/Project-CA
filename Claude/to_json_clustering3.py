import pandas as pd

def create_hierarchical_json(df):
    # Créer un dictionnaire pour stocker la structure
    result = {}
    
    # Grouper par fichier
    for file_name, file_group in df.groupby('file'):
        file_data = {'titles': []}
        current_title = None
        
        # Parcourir les lignes du groupe
        for _, row in file_group.iterrows():
            if row['Type'] == 'Titre':
                # Si c'est un titre, créer une nouvelle entrée
                if current_title is not None:
                    file_data['titles'].append(current_title)
                current_title = {
                    'title': row['text'].strip(),
                    'content': []
                }
            elif row['Type'] == 'Contenu' and current_title is not None:
                # Si c'est un contenu, l'ajouter au titre courant
                current_title['content'].append(row['text'].strip())
        
        # Ajouter le dernier titre s'il existe
        if current_title is not None:
            file_data['titles'].append(current_title)
            
        result[file_name] = file_data
    
    return result

# Lecture du CSV
df = pd.read_csv('clustering3.csv')

# Création de la structure JSON
json_structure = create_hierarchical_json(df)

# Example d'utilisation et d'affichage
import json
print(json.dumps(json_structure, ensure_ascii=False, indent=2))