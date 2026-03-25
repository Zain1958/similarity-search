# Quran Verse Similarity Search (Mutashabihat finder)
# Description

A python project which uses machine learning clustering algorithms to find *mutashabihat*—verses in the Qur'am that are highly similar in wording.

> Status: **In progress** — ML algorithms tested; Streamlit web app under development (not deployed yet).

## Motivation
There are many study resources which provide “lists of similar verses”, but those lists can be **limited in coverage** (they don't exhaustively list all verses that are similar) and **hard to explore interactively**, making them less effective for learners.

This project explores whether unsupervised ML algorithms can be leveraged to:
- find the same verse-to-verse similarities that are already in existing lists,
- find **additional** verse-to-verse similarities beyond existing lists,
- provide **fast interactive search** (type/select a verse → get the most similar verses),


Even if you’re not familiar with the Qur’an, you can think of this as a sort of **document similarity** problem on a large corpus of text.

## What it does

- Clusters all verses into groups where verses have similar wording
- Uses two clustering algorithms:
  - **K-Means**
  - **Aggolomerative clustering**
- (In progress) Produces diagrams/analysis to inspect clusters and compare the effectiveness of the 2 algorithms against each other and  existing lists 
- (In progress) Deploys a Streamlit web app for user interaction- allows users to select a verse and see all similar verses in the Qur'an, or to select a cluster and see all verses in the cluster

## Tech stack

**Python**: pandas, numpy, matplotlib, scikit-learn  
**App (WIP)**: Streamlit

---



---

 


### Installation
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

### Run the ML pipeline
> Replace with your real command(s).
```bash
python -m src.pipeline
```

### Run the Streamlit app (WIP)
> Replace with your real path/entrypoint.
```bash
streamlit run app/app.py
```

---


## Project structure (example)

> Update this section to match your repo layout.

- `data/` – dataset files (or scripts to download them)
- `notebooks/` – experiments + visual analysis
- `src/` – reusable pipeline code (preprocessing, vectorization, clustering)
- `app/` – Streamlit app (work in progress)
- `outputs/` – saved figures/results (optional)

## Results & evaluation (how to interpret output)

Because this is unsupervised clustering, “accuracy” isn’t a single number by default.
Current validation is based on:
- qualitative inspection of cluster contents
- cluster size distribution
- comparing outputs against known/curated *mutashabihat* examples (planned / partial)

Planned improvements:
- add reproducible evaluation scripts
- report clustering metrics (e.g., silhouette score) and retrieval-style metrics where applicable

---

## Roadmap

- [ ] Cleanly separate preprocessing / vectorization / clustering into a reproducible pipeline
- [ ] Add configuration (choose algorithm, number of clusters, vectorizer options)
- [ ] Streamlit UI: verse lookup + cluster browsing
- [ ] Add export (CSV/JSON) of verse → cluster and top similar verses
- [ ] Add basic tests + CI
- [ ] Deploy the Streamlit app

---

## Notes on data & text versions

This project depends on the Qur’an text source and normalization choices (e.g., diacritics, tokenization).  
Document which text source/version you use and how it is processed so results are reproducible.

---

## Disclaimer

This tool is intended to assist study by surfacing candidates for similar wording.  
It may miss relevant verses or include verses that are not meaningfully similar.

---

## License
Choose a license (MIT is common for personal projects) and add a `LICENSE` file.

---

## Contact
GitHub: https://github.com/Zain1958