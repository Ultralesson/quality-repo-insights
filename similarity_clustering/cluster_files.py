import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import defaultdict


class ClusterFiles:
    def __init__(self, folder_structure):
        self._folder_structure = folder_structure

    @staticmethod
    def __find_optimal_clusters(embeddings, max_clusters=20):
        scores = []
        best_k = 2
        for k in range(2, min(max_clusters, len(embeddings)) + 1):
            kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
            kmeans.fit(embeddings)
            labels = kmeans.labels_

            unique_labels = np.unique(labels)
            if len(unique_labels) > 1:
                try:
                    score = silhouette_score(embeddings, labels)
                    scores.append(score)
                    best_k = k
                except ValueError as e:
                    print(f"Error calculating silhouette score for {k} clusters: {e}")
            else:
                print(f"Skipping {k} clusters because only one cluster was found.")

        return best_k

    def cluster_files(self):
        file_names = []
        embeddings = []

        # Collect embeddings and file names
        for folder, files in self._folder_structure.items():
            for file_info in files:
                file_names.append(f'{folder}/{file_info["file_name"]}')
                embedding = np.array(file_info['embeddings'])
                if embedding.size > 0:
                    embeddings.append(embedding)
                else:
                    print(f"Skipping empty embedding for file: {file_info['file_name']}")

        try:
            max_length = max(e.shape[0] for e in embeddings)
            max_dim = max(e.shape[1] for e in embeddings if e.ndim == 2)

            padded_embeddings = np.array([
                np.pad(e, ((0, max_length - e.shape[0]), (0, max_dim - e.shape[1])), 'constant')
                for e in embeddings
            ])

        except Exception as e:
            raise RuntimeError(f"Error during padding: {e}")

        if padded_embeddings.ndim == 3:
            padded_embeddings = np.mean(padded_embeddings, axis=1)

        # Find optimal number of clusters
        n_clusters = self.__find_optimal_clusters(padded_embeddings)

        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
        labels = kmeans.fit_predict(padded_embeddings)

        # Group files by cluster labels
        clustered_files = defaultdict(list)
        for file_name, label in zip(file_names, labels):
            clustered_files[int(label)].append(file_name)

        return dict(clustered_files)

    @staticmethod
    def print_clustered_files(clustered_files):
        for cluster, files in clustered_files.items():
            print(f"Cluster {cluster}:")
            for file in files:
                print(f"  - {file}")
            print()
