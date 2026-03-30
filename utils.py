from scipy.cluster.hierarchy import dendrogram as _dendrogram
from scipy.cluster.hierarchy import fcluster
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import AgglomerativeClustering


def sklearn_model_to_linkage(model):
    counts = np.zeros(model.children_.shape[0]) #Model.children is a 2D array that keeps track of all of the merges
    n_samples = len(model.labels_) #An array same size as number of verses

    for i, merge in enumerate(model.children_):
        count = 0
        for child_idx in merge:
            if child_idx < n_samples: 
                count += 1
            else:
                count += counts[child_idx - n_samples]
        counts[i] = count

    # columns: child1, child2, distance, sample_count
    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)
    return linkage_matrix

def build_local_dendogram(target_chapter, target_verse, Z, k, vectorized_verses, df):
    match = df[ (df["chapter#"] == target_chapter) & (df["verse#"] == target_verse) ]
    if match.empty:
            print("Verse not found.")
    
    else:
        idx = match.index[0]
        local_labels = fcluster(Z, t=k, criterion= "maxclust")
        cluster_id = local_labels[idx]
        member_idx = np.where(local_labels = cluster_id)[0]

        print(f"Cluster {cluster_id} has {len(member_idx)} verses")

        if len(member_idx) < 2:
            print("Cluster has only 1 verse — nothing to plot.")
        elif len(member_idx) > 200:
            print(f"Cluster too large ({len(member_idx)} verses) to plot clearly. Try a higher k.")

        else:
             subset_recluster = vectorized_verses[member_idx].toArray()

             hc = AgglomerativeClustering(
                n_clusters=None,
                metric="cosine",
                linkage="complete",
                distance_threshold=0,
                compute_distances=True
             )

             hc.fit(subset_recluster)



    return fig, member_idx