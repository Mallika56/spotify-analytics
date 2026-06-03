# Spotify Content Analytics

> What drives a track's popularity? Analyzing audio features, genres, and engagement
> across a music catalog.
> **Companion project:** [Netflix content analytics](https://github.com/Mallika56/netflix-analytics) · **Cross-platform synthesis:** [Content platforms comparison](https://github.com/Mallika56/content-platforms-comparison)

**Skills demonstrated:** SQL + Python · Correlation & distribution analysis · Visualization · Data storytelling

Companion to the [Netflix Content Analytics](../netflix-analytics) project. Where Netflix
offered categorical/trend data with no engagement metric, Spotify provides **numeric audio
features** and a real **engagement signal** (`popularity`, 0–100) — enabling correlation
analysis and a cross-platform comparison.

## Business Problem

Which audio characteristics and genres are associated with higher popularity, and what
does the catalog's structure reveal about how engagement concentrates?

## Questions Asked

1. Which genres are most numerous, and which actually win on *popularity*? (These differ.)
2. What audio features correlate with popularity?
3. How do genres differ in sound (energy, danceability, valence)?
4. How is popularity distributed — a few mega-hits or an even spread?

## Tools

Python (pandas, numpy) · DuckDB (SQL on DataFrames) · matplotlib / seaborn · Jupyter

## Project Structure

```
spotify-analytics/
├── data/        # raw + cleaned data
├── notebooks/   # analysis (start: spotify_analytics_starter.ipynb)
├── sql/         # saved queries
├── visuals/     # exported charts
└── README.md
```

## How to Run

```bash
pip install pandas numpy duckdb matplotlib seaborn jupyter ipykernel
jupyter notebook notebooks/spotify_analytics_starter.ipynb
```

## Key Findings

_(Fill in from your analysis — write insights, not observations.)_

1. **Finding 1** — _what correlates with popularity_
2. **Finding 2** — _numerous vs. popular genres_
3. **Finding 3** — _how genres sound_
4. **Finding 4** — _distribution shape_

## Limitations

`popularity` is Spotify's own composite, recency-weighted metric — not raw lifetime
stream counts — so it reflects *current* attention. Observed correlations are modest
(r ≈ 0.3–0.4): real but far from deterministic.

## Data Note

The included `spotify_tracks.csv` is a **synthetic sample** built to mirror the structure
of the real Kaggle "Spotify Tracks Dataset," with realistic correlations between audio
features and popularity baked in, plus injected messiness (nulls, impossible values,
duplicates). Swap in the real Kaggle file to run the identical pipeline on actual data.
