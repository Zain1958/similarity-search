from scipy.cluster.hierarchy import dendrogram as _dendrogram
from scipy.cluster.hierarchy import fcluster
import numpy as np
import matplotlib.pyplot as plt
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

def build_local_dendrogram(target_chapter, target_verse, Z, k, vectorized_verses, df):
    match = df[(df["chapter#"] == target_chapter) & (df["verse#"] == target_verse)]
    if match.empty:
        return None, np.array([], dtype=int), "Verse not found in hierarchical dataset."

    idx = int(match.index[0])
    labels_k = fcluster(Z, t=k, criterion="maxclust")
    cluster_id = int(labels_k[idx])
    member_idx = np.where(labels_k == cluster_id)[0]

    if len(member_idx) < 2:
        return None, member_idx, "Cluster has only 1 verse, so no dendrogram can be plotted."
    if len(member_idx) > 200:
        return None, member_idx, f"Cluster too large ({len(member_idx)} verses). Increase k to get a smaller local cluster."

    subset_recluster = vectorized_verses[member_idx].toarray()

    hc_local = AgglomerativeClustering(
        n_clusters=None,
        metric="cosine",
        linkage="complete",
        distance_threshold=0,
        compute_distances=True,
    )
    hc_local.fit(subset_recluster)
    Z_local = sklearn_model_to_linkage(hc_local)

    axis_labels = [
        f"{int(df.iloc[pos]['chapter#'])}:{int(df.iloc[pos]['verse#'])}"
        for pos in member_idx
    ]

    fig, ax = plt.subplots(figsize=(max(12, len(member_idx) * 0.4), 6))
    _dendrogram(
        Z_local,
        labels=axis_labels,
        leaf_rotation=90,
        color_threshold=0.5,
        above_threshold_color="grey",
        ax=ax,
    )
    ax.set_title(
        f"Local dendogram at cut level {k} for cluster containing {target_chapter}:{target_verse}"
    )
    ax.set_ylabel("Cosine distance (when they joined)")
    fig.tight_layout()

    return fig, member_idx, f"Cluster {cluster_id} has {len(member_idx)} verses."