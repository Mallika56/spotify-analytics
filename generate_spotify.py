"""
Generate a realistic Spotify-style tracks dataset that mirrors the well-known
Kaggle 'Spotify Tracks Dataset' (audio features + popularity).

Key design goal: the audio features are NOT independent random noise. Real audio
features correlate (e.g. energy<->loudness positive; energy<->acousticness negative),
and popularity has a mild, noisy relationship with a few features. We bake those
relationships in so that correlation analysis in Phase 3+ reveals something real
instead of random static. We also inject realistic messiness (nulls, dupes,
out-of-range junk) for cleaning practice.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
N = 5000

genres = ["pop", "rock", "hip-hop", "edm", "classical", "jazz", "country",
          "r&b", "metal", "folk", "reggaeton", "lo-fi", "indie", "blues",
          "k-pop", "ambient"]
genre_weights = np.array([16, 12, 14, 10, 4, 4, 6, 7, 5, 4, 6, 5, 6, 3, 5, 3], float)
genre_weights /= genre_weights.sum()

# Per-genre "centers" for a few features so genres actually differ (realistic).
# (energy, danceability, acousticness, valence) rough centers on 0-1
genre_profile = {
    "pop":       (0.70, 0.68, 0.20, 0.60),
    "rock":      (0.78, 0.52, 0.15, 0.50),
    "hip-hop":   (0.66, 0.78, 0.18, 0.55),
    "edm":       (0.85, 0.70, 0.08, 0.55),
    "classical": (0.22, 0.30, 0.88, 0.35),
    "jazz":      (0.40, 0.55, 0.65, 0.50),
    "country":   (0.60, 0.58, 0.35, 0.58),
    "r&b":       (0.55, 0.68, 0.30, 0.52),
    "metal":     (0.92, 0.45, 0.05, 0.40),
    "folk":      (0.38, 0.50, 0.70, 0.48),
    "reggaeton": (0.78, 0.82, 0.12, 0.70),
    "lo-fi":     (0.35, 0.62, 0.55, 0.45),
    "indie":     (0.58, 0.55, 0.35, 0.50),
    "blues":     (0.45, 0.52, 0.55, 0.45),
    "k-pop":     (0.80, 0.72, 0.15, 0.65),
    "ambient":   (0.20, 0.30, 0.80, 0.30),
}

artists = [f"Artist {chr(65 + i % 26)}{i//26}" for i in range(400)]

def clip01(x):
    return float(np.clip(x, 0.0, 1.0))

rows = []
for i in range(N):
    g = rng.choice(genres, p=genre_weights)
    e_c, d_c, a_c, v_c = genre_profile[g]

    energy = clip01(rng.normal(e_c, 0.15))
    dance = clip01(rng.normal(d_c, 0.15))
    acoustic = clip01(rng.normal(a_c, 0.18))
    valence = clip01(rng.normal(v_c, 0.18))
    # loudness correlates positively with energy (dB, negative scale ~ -60..0)
    loudness = round(-2 + (energy * -1 + 1) * -18 + rng.normal(0, 2), 2)
    loudness = float(np.clip(loudness, -40, 0))
    tempo = round(float(np.clip(rng.normal(118, 28), 50, 210)), 2)
    duration_ms = int(np.clip(rng.normal(210000, 60000), 40000, 600000))
    speechiness = clip01(rng.normal(0.08 + (0.25 if g == "hip-hop" else 0), 0.06))
    instrumentalness = clip01(
        rng.normal(0.6 if g in ("classical", "ambient", "lo-fi") else 0.05, 0.2)
    )

    # Popularity: mild, NOISY relationship with a few features + genre effect.
    # Deliberately weak so the lesson is "correlation is real but modest", not fake-strong.
    genre_pop_boost = {"pop": 12, "hip-hop": 10, "reggaeton": 8, "k-pop": 9,
                       "edm": 5}.get(g, 0)
    base = (40
            + 18 * dance
            + 12 * energy
            - 10 * instrumentalness
            + genre_pop_boost
            + rng.normal(0, 14))   # big noise term = realistic weak signal
    popularity = int(np.clip(base, 0, 100))

    rows.append({
        "track_id": f"t{i+1}",
        "track_name": f"Track {i+1}",
        "artist": rng.choice(artists),
        "genre": g,
        "popularity": popularity,
        "danceability": round(dance, 3),
        "energy": round(energy, 3),
        "loudness": loudness,
        "speechiness": round(speechiness, 3),
        "acousticness": round(acoustic, 3),
        "instrumentalness": round(instrumentalness, 3),
        "valence": round(valence, 3),
        "tempo": tempo,
        "duration_ms": duration_ms,
    })

df = pd.DataFrame(rows)

# ---- Inject realistic messiness ----
# 1) Nulls in a few feature columns
for col, frac in [("tempo", 0.02), ("popularity", 0.015), ("genre", 0.01)]:
    idx = df.sample(frac=frac, random_state=1).index
    df.loc[idx, col] = np.nan

# 2) A handful of out-of-range junk values to catch in cleaning
junk = df.sample(12, random_state=2).index
df.loc[junk, "tempo"] = 0.0          # impossible tempo
df.loc[df.sample(8, random_state=3).index, "duration_ms"] = -1  # impossible duration

# 3) Exact duplicate rows
df = pd.concat([df, df.sample(20, random_state=4)], ignore_index=True)

df.to_csv("/home/claude/spotify_tracks.csv", index=False)
print("Rows:", len(df))
print("\nNulls:\n", df.isnull().sum())
print("\nPopularity describe:\n", df["popularity"].describe().round(1))
print("\nGenre counts (top):\n", df["genre"].value_counts().head())
print("\nQuick correlation sanity (popularity vs features):")
print(df[["popularity","danceability","energy","instrumentalness"]].corr()["popularity"].round(3))
