SELECT name FROM songs;

SELECT name FROM songs
ORDER BY tempo ASC;

SELECT name FROM songs
ORDER BY duration_ms DESC
LIMIT 5;

SELECT name FROM songs
WHERE danceability > 0.75
AND energy > 0.75
AND valence > 0.75;

SELECT AVG(energy)
FROM songs;

SELECT name FROM songs
WHERE artist_id =
(SELECT id name FROM artists
WHERE name = 'Post Malone');

SELECT AVG(energy)
FROM songs
WHERE artist_id =
(SELECT id name FROM artists
WHERE name = 'Drake');

SELECT name FROM songs
WHERE name LIKE ("%feat.%");
