-- Spotify Content Analytics — SQL queries (DuckDB against the cleaned `df`)
-- Q1-Q9 as run in notebooks/spotify_analytics_starter.ipynb (Phase 3).

-- Q1: Track count by genre
SELECT genre, COUNT(*) AS tracks
FROM df
GROUP BY genre
ORDER BY tracks DESC;

-- Q2: Average popularity by genre (engagement angle)
SELECT genre,
       COUNT(*) AS tracks,
       ROUND(AVG(popularity), 1) AS avg_popularity
FROM df
GROUP BY genre
ORDER BY avg_popularity DESC;

-- Q3: Average audio features by genre
SELECT genre,
       ROUND(AVG(danceability), 3) AS danceability,
       ROUND(AVG(energy), 3)       AS energy,
       ROUND(AVG(acousticness), 3) AS acousticness,
       ROUND(AVG(valence), 3)      AS valence
FROM df
GROUP BY genre
ORDER BY energy DESC;

-- Q4: Top 10 most popular tracks
SELECT track_name, artist, genre, popularity
FROM df
ORDER BY popularity DESC
LIMIT 10;

-- Q5: Loudness vs energy sanity check
SELECT genre,
       ROUND(AVG(loudness), 2) AS avg_loudness,
       ROUND(AVG(energy), 2)   AS avg_energy
FROM df
GROUP BY genre
ORDER BY avg_energy DESC;

-- Q6: "Happy vs sad" genres by valence
SELECT genre, ROUND(AVG(valence), 3) AS avg_valence
FROM df
GROUP BY genre
ORDER BY avg_valence DESC;

-- Q7: Popularity buckets (CASE statement)
SELECT
    CASE
        WHEN popularity < 40 THEN 'Low'
        WHEN popularity < 70 THEN 'Medium'
        ELSE 'High'
    END AS popularity_tier,
    COUNT(*) AS tracks
FROM df
GROUP BY popularity_tier
ORDER BY
    CASE popularity_tier
        WHEN 'Low' THEN 1
        WHEN 'Medium' THEN 2
        ELSE 3
    END;

-- Q8: Top track per genre by popularity (window function)
WITH ranked AS (
    SELECT track_name, artist, genre, popularity,
           ROW_NUMBER() OVER (PARTITION BY genre ORDER BY popularity DESC) AS rk
    FROM df
)
SELECT genre, track_name, artist, popularity
FROM ranked
WHERE rk = 1
ORDER BY popularity DESC;

-- Q9: Each genre vs the overall average popularity
WITH overall AS (
    SELECT AVG(popularity) AS overall_avg FROM df
)
SELECT genre,
       ROUND(AVG(df.popularity), 1) AS genre_avg,
       ROUND((SELECT overall_avg FROM overall), 1) AS overall_avg,
       ROUND(AVG(df.popularity) - (SELECT overall_avg FROM overall), 1) AS diff
FROM df
GROUP BY genre
ORDER BY diff DESC;
