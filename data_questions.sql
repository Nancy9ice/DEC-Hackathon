--  1. How many countries speaks French? ANSWER = 46
SELECT COUNT(DISTINCT c.country_name) AS num_countries
FROM countries c
JOIN country_languages cl ON c.country_id = cl.country_id
JOIN languages l ON cl.language_id = l.language_id
WHERE l.language_name = 'French';

--  2. How many countries speak English? ANSWER = 91
SELECT COUNT(DISTINCT c.country_name) AS num_countries
FROM countries c
JOIN country_languages cl ON c.country_id = cl.country_id
JOIN languages l ON cl.language_id = l.language_id
WHERE l.language_name = 'English';

--  3. How many countries have more than one official language? ANSWER = 96
SELECT COUNT(country_id) AS num_countries
FROM (
    SELECT country_id, COUNT(language_id) AS num_languages
    FROM country_languages
    GROUP BY country_id
    HAVING COUNT(language_id) > 1
) AS multi_lang_countries;

--  4. How many countries have the Euro as their official currency? ANSWER = 36
SELECT COUNT(*) AS num_countries
FROM countries
WHERE currency_code = 'EUR';

--  5. How many countries are from Western Europe? ANSWER = 8
SELECT COUNT(*) AS num_countries
FROM countries
WHERE sub_region = 'Western Europe';

--  6. How many countries have not yet gained independence? ANSWER = 55
SELECT COUNT(*) AS num_countries
FROM countries
WHERE independence = FALSE;

--  7. How many distinct continents and how many countries from each? ANSWER = 7 continents
SELECT continents, COUNT(*) AS num_countries
FROM countries
GROUP BY continents;

--  8. How many countries start the week on a day other than Monday? ANSWER = 21
SELECT COUNT(*) AS num_countries
FROM countries
WHERE start_of_week != 'monday';

--  9. How many countries are not United Nations members? ANSWER = 57
SELECT COUNT(*) AS num_countries
FROM countries
WHERE united_nations_member = FALSE;

--  10. How many countries are United Nations members? ANSWER = 192
SELECT COUNT(*) AS num_countries
FROM countries
WHERE united_nations_member = TRUE;

--  11. At least 2 countries with the lowest population for each continent? ANSWER = 
SELECT continents, country_name, population
FROM (
    SELECT continents, country_name, population,
           ROW_NUMBER() OVER (PARTITION BY continents ORDER BY population ASC) AS rank
    FROM countries
) AS ranked_countries
WHERE rank <= 2;

--  12. Top 2 countries with the largest area for each continent? ANSWER =
SELECT continents, country_name, area
FROM (
    SELECT continents, country_name, area,
           ROW_NUMBER() OVER (PARTITION BY continents ORDER BY area DESC) AS rank
    FROM countries
) AS ranked_countries
WHERE rank <= 2;

--  13. Top 5 countries with the largest area? ANSWER =
SELECT country_name, area
FROM countries
ORDER BY area DESC
LIMIT 5;

--  14. Top 5 countries with the lowest area? ANSWER =
SELECT country_name, area
FROM countries
ORDER BY area ASC
LIMIT 5;

