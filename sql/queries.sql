-- Spotify Content Analytics — SQL queries (DuckDB against the cleaned `df`)
-- Q1-Q3 worked; add Q4-Q9 as you write them.

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

-- Q8 (reference): top track per genre by popularity (window function)
WITH ranked AS (
    SELECT track_name, artist, genre, popularity,
           ROW_NUMBER() OVER (PARTITION BY genre ORDER BY popularity DESC) AS rk
    FROM df
)
SELECT genre, track_name, artist, popularity
FROM ranked
WHERE rk = 1
ORDER BY popularity DESC;
