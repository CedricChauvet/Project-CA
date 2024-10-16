import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Charger le fichier CSV
df = pd.read_csv('dataset-print3.csv')

def apply_clustering(group):
    # Créer un tableau 2D avec font_size et is_bold
    features = np.column_stack((group['font_size'], group['is_bold'].astype(int)))
    
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Utiliser 2 clusters : un pour les titres (gras ou grande taille) et un pour le contenu
    kmeans = KMeans(n_clusters=2, random_state=42)
    group['Cluster'] = kmeans.fit_predict(features_scaled)
    
    # Identifier le cluster des titres (celui avec la plus grande moyenne de taille de police ou le plus de texte en gras)
    cluster_means = group.groupby('Cluster')[['font_size', 'is_bold']].mean()
    title_cluster = cluster_means.idxmax().mode().values[0]
    
    # Attribuer les types
    group['Type'] = np.where(group['Cluster'] == title_cluster, 'Titre', 'Contenu')
    
    # Ajuster pour les sous-titres : les titres non gras avec une taille de police inférieure à la moyenne des titres
    title_font_mean = group[group['Type'] == 'Titre']['font_size'].mean()
    group.loc[(group['Type'] == 'Titre') & (~group['is_bold']) & (group['font_size'] < title_font_mean), 'Type'] = 'Sous-titre'
    
    return group

# Appliquer le clustering à chaque fichier source séparément
df_clustered = df.groupby('file_number').apply(apply_clustering).reset_index(drop=True)

# Visualiser les résultats
plt.figure(figsize=(15, 8))
for file_num in df_clustered['file_number'].unique():
    file_data = df_clustered[df_clustered['file_number'] == file_num]
    plt.scatter(file_data['font_size'], file_data['is_bold'], 
                c=file_data['Type'].map({'Titre': 'red', 'Sous-titre': 'green', 'Contenu': 'blue'}),
                label=f'File {file_num}', alpha=0.7)

plt.xlabel('Taille de police')
plt.ylabel('Est en gras')
plt.title('Clustering basé sur la taille de police et le gras pour chaque fichier source')
plt.legend()
plt.show()

# Afficher un aperçu des résultats
print(df_clustered[['file_number', 'font_size', 'is_bold', 'Type']].head(20))

# Compter le nombre d'éléments de chaque type pour chaque fichier
print(df_clustered.groupby(['file_number', 'Type']).size().unstack(fill_value=0))

# Sauvegarder le résultat
df_clustered.to_csv('clustering3.csv', index=False)
df_clustered.head(100).to_csv('clustering3_100.csv', index=False)
