import streamlit as st
import pandas as pd

# 1. Load Data
@st.cache_data
def load_data():
    return pd.read_csv("data/clustered_verses.csv")

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
    st.write("This area is reserved for your next algorithm!")