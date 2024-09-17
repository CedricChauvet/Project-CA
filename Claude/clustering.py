"""
Clustering basé sur la taille de police, ne fonction pas
il ne pas pas en compte le fait que chaque fichier source a une taille de police différente
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


# Charger le fichier CSV
df = pd.read_csv('dataset-cluster.csv')

# Extraire la colonne font_size
font_sizes = df['font_size'].values.reshape(-1, 1)

# Normaliser les tailles de police
scaler = StandardScaler()
font_sizes_scaled = scaler.fit_transform(font_sizes)

# Appliquer K-means
n_clusters = 2  # Vous pouvez ajuster ce nombre selon vos besoins
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(font_sizes_scaled)

# Afficher un aperçu des résultats
print(df[['font_size', 'Cluster']].head(100))

# Compter le nombre d'éléments dans chaque cluster
print(df['Cluster'].value_counts())

# Visualiser les résultats
plt.figure(figsize=(10, 6))
for i in range(n_clusters):
    cluster_data = df[df['Cluster'] == i]
    plt.scatter(cluster_data.index, cluster_data['font_size'], label=f'Cluster {i}')

plt.xlabel('Index de ligne')
plt.ylabel('Taille de police')
plt.title('Clustering basé sur la taille de police')
plt.legend()
plt.show()

# Identifier les clusters (vous devrez peut-être ajuster ceci en fonction de vos résultats)
mean_sizes = df.groupby('Cluster')['font_size'].mean().sort_values(ascending=False)
df['Type'] = df['Cluster'].map({
    mean_sizes.index[0]: 'Titre',
    mean_sizes.index[1]: 'Sous-titre',
})

# Afficher un aperçu des résultats finaux
print(df[['font_size', 'Type']].head(200))

# Sauvegarder le résultat
df.to_csv('fichier_avec_classification.csv', index=False)