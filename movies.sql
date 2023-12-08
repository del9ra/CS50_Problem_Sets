SELECT title FROM movies
WHERE year = 2008;

SELECT birth from people
WHERE name = 'Emma Stone';

SELECT title FROM movies
WHERE year >= 2018
ORDER BY title ASC;

SELECT COUNT(movie_id) FROM ratings
WHERE rating = 10.0;

SELECT title, year
FROM movies
WHERE title LIKE "Harry Potter%"
ORDER BY year ASC;

SELECT AVG(rating)
FROM ratings
WHERE movie_id IN
(SELECT id FROM movies
WHERE year = 2012);

-- joined two columns(title, rating) from two different tables(movies, ratings)
SELECT title, rating FROM movies, ratings
--on the base of same IDs
WHERE movies.id = ratings.movie_id
AND rating IS NOT NULL
AND year = 2010
--order movies by rating desc and movies with the same rating alphabetically by title
ORDER BY rating DESC, title ASC;

SELECT name FROM people
WHERE id in
(SELECT person_id FROM stars
WHERE movie_id in
(SELECT id FROM movies
WHERE title = 'Toy Story'));

--escape duplicates
SELECT DISTINCT(name) FROM people
--in - search for multiple values
WHERE id in
(SELECT person_id FROM stars
WHERE movie_id in
(SELECT id FROM movies
WHERE year = 2004))
ORDER BY birth;

SELECT DISTINCT(name) FROM people
-- connecting people table with directors table
JOIN directors ON people.id = directors.person_id
--connecting ratings with directors table
JOIN ratings ON ratings.movie_id = directors.movie_id
WHERE rating >= 9.0;

SELECT title FROM movies
-- join two tables
JOIN ratings on ratings.movie_id = movies.id
--in specifies multiple values
WHERE movie_id in
--retrieve id from stars
(SELECT movie_id FROM stars
WHERE person_id =
--retrieve person id from people
(SELECT id FROM people
WHERE name = "Chadwick Boseman"))
ORDER BY rating DESC
--top 5
LIMIT 5;

--output titles of movies
SELECT title FROM movies
--retrieve movie_id
JOIN stars on movies.id = stars.movie_id
--found names of actors, people id through stars table
JOIN people on stars.person_id = people.id
--got into people to extract id
WHERE name IN ("Jennifer Lawrence", "Bradley Cooper")
--groupped movie titles
GROUP BY title
--extract movies where both(2) actors took part
HAVING COUNT(name) = 2;

--output names of actors
SELECT name FROM people
WHERE id in
--retrieve actors' id
(SELECT person_id FROM stars
WHERE movie_id in
--retrieve movies id
(SELECT movie_id FROM stars
-- extract Kevin's id
JOIN people on stars.person_id = people.id
WHERE name = 'Kevin Bacon'
AND birth = 1958))
-- exclude Kevin himself
AND NOT name = "Kevin Bacon";
