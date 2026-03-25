import streamlit as st
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import fcluster

# 1. Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/clustered_verses.csv")


@st.cache_data
def load_hierarchical_data():
    verses_df = pd.read_csv("data/hc_verses.csv")
    linkage_matrix = np.load("data/hc_linkage.npy")
    return verses_df, linkage_matrix

df = load_data()

st.title("🕋 Quranic Mutashabihaat Explorer")

# --- TOP LEVEL TABS ---
tab_kmeans, tab_hierarchical = st.tabs(["K-Means", "Hierarchical"])

# --- K-MEANS SECTION ---
with tab_kmeans:
    # 2. NESTED TABS (Only visible when K-Means is selected)
    subtab1, subtab2 = st.tabs(["🔍 Search Ayah", "📊 Browse Clusters"])
    
    with subtab1:
        st.subheader("Find which cluster an Ayah belongs to")
        col1, col2 = st.columns(2)
        with col1:
            s_num = st.number_input("Surah", 1, 114, 1, key="km_s")
        with col2:
            a_num = st.number_input("Ayah", 1, 286, 1, key="km_a")
        
        # Search logic
        match = df[(df['chapter#'] == s_num) & (df['verse#'] == a_num)]
        if not match.empty:
            c_id = match['cluster'].values[0]
            st.info(f"This verse is in K-Means **Cluster {c_id}**")
            st.dataframe(df[df['cluster'] == c_id][['chapter#', 'verse#', 'verse']])

    with subtab2:
        st.subheader("Explore the Quran's thematic groups")
        # Use the sidebar only for this sub-tab
        cluster_selection = st.sidebar.slider("Select K-Means Cluster", 0, 69, 0)
        
        st.write(f"Showing all verses for **Cluster {cluster_selection}**")
        st.dataframe(df[df['cluster'] == cluster_selection][['chapter#', 'verse#', 'verse']])

# --- HIERARCHICAL SECTION ---
with tab_hierarchical:
    st.header("Hierarchical Results")

    try:
        h_df, Z = load_hierarchical_data()
    except Exception:
        st.warning("Missing hierarchical files. Save `data/hc_verses.csv` and `data/hc_linkage.npy` from your notebook first.")
        st.stop()

    st.subheader("Find cluster for a verse")

    c1, c2 = st.columns(2)
    with c1:
        h_s_num = st.number_input("Chapter", min_value=1, max_value=114, value=1, key="h_s")
    with c2:
        h_a_num = st.number_input("Verse", min_value=1, max_value=286, value=1, key="h_a")

    max_k = min(len(h_df), 2000)
    k = st.slider("Cluster layer (number of groups)", min_value=2, max_value=max_k, value=300)

    labels_k = fcluster(Z, t=k, criterion="maxclust")

    match = h_df[(h_df["chapter#"] == h_s_num) & (h_df["verse#"] == h_a_num)]
    if match.empty:
        st.error("Verse not found in hierarchical dataset.")
    else:
        idx = int(match.index[0])
        cluster_id = int(labels_k[idx])
        cluster_rows = h_df[labels_k == cluster_id]

        st.info(f"Verse {h_s_num}:{h_a_num} is in hierarchical cluster {cluster_id} at k={k}.")
        st.write(f"Cluster size: {len(cluster_rows)}")
        st.dataframe(cluster_rows[["chapter#", "verse#", "verse"]])