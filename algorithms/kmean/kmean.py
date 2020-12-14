from sklearn.cluster import KMeans
import numpy as np

class KMeanClusterer ():
    def __init__(self, X: np.ndarray):
        kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
        print(kmeans.labels_)
        print(kmeans.predict([[0, 0], [12, 3]]))
        print(kmeans.cluster_centers_)