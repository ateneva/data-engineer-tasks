
--
-- View structure for view `customer_list`
--

CREATE VIEW customer_list
AS
SELECT 
    cu.customer_id AS ID, 
    CONCAT(cu.first_name, _utf8mb4' ', cu.last_name) AS name, 
    a.address AS address, 
    a.postal_code AS `zip code`,
	a.phone AS phone, 
    city.city AS city, 
    country.country AS country, 
    IF(cu.active, _utf8mb4'active',_utf8mb4'') AS notes, 
    cu.store_id AS SID
FROM customer AS cu 
    JOIN address AS a 
        ON cu.address_id = a.address_id JOIN city ON a.city_id = city.city_id
	JOIN country 
        ON city.country_id = country.country_id;

--
-- View structure for view `film_list`
--

CREATE VIEW film_list
AS
SELECT 
    film.film_id AS FID, 
    film.title AS title, 
    film.description AS description, 
    category.name AS category, 
    film.rental_rate AS price,
	film.length AS length, 
    film.rating AS rating, 
    GROUP_CONCAT(CONCAT(actor.first_name, _utf8mb4' ', actor.last_name) SEPARATOR ', ') AS actors
FROM category 
    LEFT JOIN film_category 
        ON category.category_id = film_category.category_id 
    LEFT JOIN film 
        ON film_category.film_id = film.film_id
        JOIN film_actor ON film.film_id = film_actor.film_id
	JOIN actor ON film_actor.actor_id = actor.actor_id
GROUP BY film.film_id, category.name;

--
-- View structure for view `nicer_but_slower_film_list`
--

CREATE VIEW nicer_but_slower_film_list
AS
SELECT 
    film.film_id AS FID, 
    film.title AS title, 
    film.description AS description, 
    category.name AS category, 
    film.rental_rate AS price,
	film.length AS length, 
    film.rating AS rating, 
    GROUP_CONCAT(CONCAT(CONCAT(UCASE(SUBSTR(actor.first_name,1,1)),
	LCASE(SUBSTR(actor.first_name,2,LENGTH(actor.first_name))),_utf8mb4' ',
    CONCAT(UCASE(SUBSTR(actor.last_name,1,1)),
	    LCASE(SUBSTR(actor.last_name,2,LENGTH(actor.last_name)))))) SEPARATOR ', ') AS actors
FROM category 
    LEFT JOIN film_category 
        ON category.category_id = film_category.category_id 
    LEFT JOIN film
     ON film_category.film_id = film.film_id
        JOIN film_actor ON film.film_id = film_actor.film_id
	JOIN actor 
        ON film_actor.actor_id = actor.actor_id
GROUP BY film.film_id, category.name;

--
-- View structure for view `staff_list`
--

CREATE VIEW staff_list
AS
SELECT 
    s.staff_id AS ID, 
    CONCAT(s.first_name, _utf8mb4' ', s.last_name) AS name, 
    a.address AS address, 
    a.postal_code AS `zip code`, 
    a.phone AS phone,
	city.city AS city, 
    country.country AS country, 
    s.store_id AS SID
FROM staff AS s 
    JOIN address AS a 
        ON s.address_id = a.address_id 
    JOIN city 
        ON a.city_id = city.city_id
	JOIN country 
        ON city.country_id = country.country_id;

--
-- View structure for view `sales_by_store`
--

CREATE VIEW sales_by_store
AS
SELECT
CONCAT(c.city, _utf8mb4',', cy.country) AS store
, CONCAT(m.first_name, _utf8mb4' ', m.last_name) AS manager
, SUM(p.amount) AS total_sales
FROM payment AS p
INNER JOIN rental AS r 
    ON p.rental_id = r.rental_id
INNER JOIN inventory AS i 
    ON r.inventory_id = i.inventory_id
INNER JOIN store AS s 
    ON i.store_id = s.store_id
INNER JOIN address AS a 
    ON s.address_id = a.address_id
INNER JOIN city AS c 
    ON a.city_id = c.city_id
INNER JOIN country AS cy 
    ON c.country_id = cy.country_id
INNER JOIN staff AS m 
    ON s.manager_staff_id = m.staff_id
GROUP BY s.store_id
ORDER BY cy.country, c.city;

--
-- View structure for view `sales_by_film_category`
--
-- Note that total sales will add up to >100% because
-- some titles belong to more than 1 category
--

CREATE VIEW sales_by_film_category
AS
SELECT
c.name AS category
, SUM(p.amount) AS total_sales
FROM payment AS p
INNER JOIN rental AS r 
    ON p.rental_id = r.rental_id
INNER JOIN inventory AS i 
    ON r.inventory_id = i.inventory_id
INNER JOIN film AS f 
    ON i.film_id = f.film_id
INNER JOIN film_category AS fc 
    ON f.film_id = fc.film_id
INNER JOIN category AS c 
    ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY total_sales DESC;

--
-- View structure for view `actor_info`
--

CREATE DEFINER=CURRENT_USER SQL SECURITY INVOKER VIEW actor_info
AS
SELECT
a.actor_id,
a.first_name,
a.last_name,
GROUP_CONCAT(DISTINCT CONCAT(c.name, ': ',
		(SELECT GROUP_CONCAT(f.title ORDER BY f.title SEPARATOR ', ')
                    FROM dvd.film f
                    INNER JOIN dvd.film_category fc
                      ON f.film_id = fc.film_id
                    INNER JOIN dvd.film_actor fa
                      ON f.film_id = fa.film_id
                    WHERE fc.category_id = c.category_id
                    AND fa.actor_id = a.actor_id
                 )
             )
             ORDER BY c.name SEPARATOR '; ')
AS film_info
FROM dvd.actor a
LEFT JOIN dvd.film_actor fa
  ON a.actor_id = fa.actor_id
LEFT JOIN dvd.film_category fc
  ON fa.film_id = fc.film_id
LEFT JOIN dvd.category c
  ON fc.category_id = c.category_id
GROUP BY a.actor_id, a.first_name, a.last_name;
