from sklearn.cluster import KMeans
import numpy as np
from flask import Response, stream_with_context
from scipy.spatial import distance
import sys
import time

class KMeanClusterer ():
    def __init__(self, X: np.ndarray, k: int=2, initializer: str='forgy'):
        # kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
        # print(kmeans.labels_)
        # print(kmeans.predict([[0, 0], [12, 3]]))
        # print(kmeans.cluster_centers_)
        self.dim = X.shape[1]
        self.n = X.shape[0]
        self.k = k
        self.data = X.copy()
        self.clusters = np.asarray([0] * self.n, dtype=np.int32)
        self.centroids = np.asarray([[0.0] * self.dim] * self.k, dtype=np.float64)

        if initializer == 'forgy':
            self.forgy_initialize()
        else:
            self.forgy_initialize()

    def forgy_initialize(self):
        s = set()
        for i in range(self.k):
            k = np.random.randint(0, self.n - 1)
            while k in s:
                k = np.random.randint(0, self.k - 1)
            s.add(k)
            self.centroids[i] = self.data[k].copy()

    def euclidean(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """ Given 2 vector, compute the distance between them.

        Args:
            v1 (np.ndarray): Shape (dim,)
            v2 (np.ndarray): Shape (dim,)

        Returns:
            float: Euclidean distance
        """
        return np.linalg.norm(v1 - v2)
        
        # return float(distance.euclidean(v1, v2))
        

    def wcss(self) -> float:
        """[summary]

        Returns:
            float: [description]
        """
        g :float= 0.0
        for vector, cluster_id in zip(self.data, self.clusters):
            g += self.euclidean(vector, self.centroids[cluster_id]) ** 2
        return g

    def assign_cluster(self) -> bool:
        """[summary]

        Returns:
            bool: [description]
        """
        changed = False
        # loop through all data points.
        for id, point in enumerate(self.data):
            min_distance = sys.maxsize
            # loop through all centroids to see which one has the closest distance.
            for centroid_id, centroid in enumerate(self.centroids):
                distance = self.euclidean(point, centroid)
                if distance < min_distance:
                    min_distance = distance
                    self.clusters[id] = centroid_id
                    changed = True
        return changed

    def compute_centroids(self) -> None:
        """[summary]
        """
        # For each cluster, compute the mean point.
        # Assign new centroid for each cluster.
        for cluster_id in range(self.k):
            all_points_id = self.clusters[np.where(self.clusters == cluster_id)]
            all_points = np.asarray([self.data[id] for id in all_points_id])
            self.centroids[cluster_id] = np.mean(all_points, axis=0)

    def step(self) -> None:
        """[summary]
        """
        wcss = self.wcss()
        while True:
            self.assign_cluster()
            self.compute_centroids()
            newWcss = self.wcss()
            if newWcss >= wcss:
                break
            wcss = newWcss

    def iterate(self) -> None:
        pass

    def clusterize(self) -> None:
        """ Clusterize and assign new cluster
        """
        pass

    def __str__(self):
        return f"Clusters: \n{self.clusters}\n Centroids:\n{self.centroids}\n"

    def stream(self) -> Response:
        self.step()
        # print(self.__str__())
        def generate():
            
            wcss = self.wcss()
            
            while True:
                time.sleep(0.01)
            # for i in range(5):
                self.assign_cluster()
                self.compute_centroids()
                newWcss = self.wcss()
                
                print("Current wcss: " + str(wcss))
                print("NEw wcss: " + str(newWcss))
                print(self.__str__())
                if newWcss >= wcss:
                    return
                wcss = newWcss
                print("Get here")
                yield self.__str__()

            # for i in range(5):
            #     # print("Hello")
            #     time.sleep(1)
            #     yield self.__str__()

        return Response(stream_with_context(generate()))