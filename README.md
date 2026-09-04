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
pip install -r requirements.txt
jupyter notebook notebooks/spotify_analytics_starter.ipynb
```

Regenerate the synthetic dataset with `python generate_spotify.py` (writes
`data/spotify_tracks.csv`). Run the test suite with `pytest`.

## Key Findings

1. **Danceable, energetic, and vocal tracks win; tempo is irrelevant.** Popularity
   correlates positively with danceability (r = 0.43), energy (0.35), and loudness
   (0.33), and negatively with acousticness (−0.34) and instrumentalness (−0.33).
   Tempo shows essentially no relationship (r = 0.01).
2. **Volume and popularity diverge.** The most-catalogued genres are pop, hip-hop,
   and rock, but ranked by *average* popularity, hip-hop matches pop despite 9%
   fewer tracks, while rock trails pop by 13 points despite a large catalog. What
   gets made is not what gets streamed.
3. **Popularity is bell-shaped around the mid-60s**, not a long-tail skew — mean
   ≈ median (61.1 / 62.0), with most tracks showing at least some traction rather
   than a few mega-hits dominating.
4. **Volatility varies sharply by genre.** EDM, k-pop, hip-hop, and reggaeton have
   the widest popularity spread (biggest gap between hits and misses); other
   genres cluster tightly around their average — a distinction that matters more
   than the average alone for anyone betting on a genre.

See `notebooks/spotify_analytics_starter.ipynb` (Phase 5) for the full write-up,
including limitations on what audio features can and can't predict.

## Limitations

`popularity` is Spotify's own composite, recency-weighted metric — not raw lifetime
stream counts — so it reflects *current* attention. Observed correlations are modest
(r ≈ 0.3–0.4): real but far from deterministic.

## Data Note

The included `spotify_tracks.csv` is a **synthetic sample** built to mirror the structure
of the real Kaggle "Spotify Tracks Dataset," with realistic correlations between audio
features and popularity baked in, plus injected messiness (nulls, impossible values,
duplicates). Swap in the real Kaggle file to run the identical pipeline on actual data.
