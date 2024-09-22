import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Charger le fichier CSV
df = pd.read_csv('./dataset-print2.csv')

def apply_clustering(group):
    font_sizes = group['font_size'].values.reshape(-1, 1)
    scaler = StandardScaler()
    font_sizes_scaled = scaler.fit_transform(font_sizes)
    
    # Commencer avec 3 clusters, réduire si nécessaire
    for n_clusters in range(3, 0, -1):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        group['Cluster'] = kmeans.fit_predict(font_sizes_scaled)
        
        mean_sizes = group.groupby('Cluster')['font_size'].mean().sort_values(ascending=False)
        
        if len(mean_sizes) == n_clusters:
            break
    
    # Attribuer les types en fonction du nombre de clusters trouvés
    if len(mean_sizes) == 3:
        cluster_types = {
            mean_sizes.index[0]: 'Titre',
            mean_sizes.index[1]: 'Sous-titre',
            mean_sizes.index[2]: 'Contenu'
        }
    elif len(mean_sizes) == 2:
        cluster_types = {
            mean_sizes.index[0]: 'Titre',
            mean_sizes.index[1]: 'Sous-titre'
        }
    else:  # Si un seul cluster
        cluster_types = {mean_sizes.index[0]: 'probleme'}
    
    group['Type'] = group['Cluster'].map(cluster_types)
    
    return group

# Appliquer le clustering à chaque fichier source séparément
df_clustered = df.groupby('file_number').apply(apply_clustering).reset_index(drop=True)

# Visualiser les résultats
plt.figure(figsize=(15, 8))
for file_num in df_clustered['file_number'].unique():
    file_data = df_clustered[df_clustered['file_number'] == file_num]
    plt.scatter(file_data.index, file_data['font_size'], 
                label=f'File {file_num}', alpha=0.7)

plt.xlabel('Index de ligne')
plt.ylabel('Taille de police')
plt.title('Clustering basé sur la taille de police pour chaque fichier source')
plt.legend()
plt.grid(True)
plt.show()

# Afficher un aperçu des résultats
print("file", file_num, df_clustered[['file_number', 'font_size', 'Type']][90:170])

# Compter le nombre d'éléments de chaque type pour chaque fichier
# print(df_clustered.groupby(['file_number', 'Type']).size().unstack(fill_value=0))

# Sauvegarder le résultat
df_clustered.to_csv('sortie1.csv', index=False)