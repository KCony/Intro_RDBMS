Tech stack
==========
https://www.postgresql.org/download/
https://dbeaver.io/download/


Data source
===========
Data.gov
Farmers Markets Directory and Geographic Data https://catalog.data.gov/dataset/farmers-markets-directory-and-geographic-data
https://apps.ams.usda.gov/FarmersMarketsExport/ExcelExport.aspx



PostgreSQL example
==================

Creating and population the database
------------------------------------

CREATE DATABASE farmers_markets;

-- public.categories definition

-- Drop table

-- DROP TABLE categories;

CREATE TABLE categories (
	category_id serial4 NOT NULL,
	category varchar NULL,
	CONSTRAINT categories_pk PRIMARY KEY (category_id)
);


-- public.states definition

-- Drop table

-- DROP TABLE states;

CREATE TABLE states (
	state_id serial4 NOT NULL,
	state_full varchar NULL,
	state_abbr bpchar(2) NOT NULL,
	CONSTRAINT states_pk PRIMARY KEY (state_id)
);


-- public.users definition

-- Drop table

-- DROP TABLE users;

CREATE TABLE users (
	user_id serial4 NOT NULL,
	fname varchar NULL,
	lname varchar NULL,
	username varchar NOT NULL,
	password_hash varchar NOT NULL,
	CONSTRAINT users_pk PRIMARY KEY (user_id)
);


-- public.cities definition

-- Drop table

-- DROP TABLE cities;

CREATE TABLE cities (
	city_id serial4 NOT NULL,
	city varchar NOT NULL,
	state_id int4 NOT NULL,
	CONSTRAINT cities_pk PRIMARY KEY (city_id),
	CONSTRAINT cities_states_fk FOREIGN KEY (state_id) REFERENCES states(state_id)
);


-- public.markets definition

-- Drop table

-- DROP TABLE markets;

CREATE TABLE markets (
	market_id int4 NOT NULL,
	market_name varchar NULL,
	street varchar NULL,
	city int4 NULL,
	state int4 NULL,
	zip int4 NULL,
	lat float4 NULL,
	lon float4 NULL,
	CONSTRAINT markets_pk PRIMARY KEY (market_id),
	CONSTRAINT markets_cities_fk FOREIGN KEY (city) REFERENCES cities(city_id),
	CONSTRAINT markets_states_fk FOREIGN KEY (state) REFERENCES states(state_id)
);


-- public.markets_categories definition

-- Drop table

-- DROP TABLE markets_categories;

CREATE TABLE markets_categories (
	market_category_id int4 NOT NULL,
	market_id int4 NOT NULL,
	category_id int4 NOT NULL,
	CONSTRAINT markets_categories_pk PRIMARY KEY (market_category_id),
	CONSTRAINT markets_categories_categories_fk FOREIGN KEY (category_id) REFERENCES categories(category_id),
	CONSTRAINT markets_categories_markets_fk FOREIGN KEY (market_id) REFERENCES markets(market_id)
);


-- public.reviews definition

-- Drop table

-- DROP TABLE reviews;

CREATE TABLE reviews (
	review_id serial4 NOT NULL,
	user_id int4 NOT NULL,
	market_id int4 NOT NULL,
	date_time date NOT NULL,
	score int2 NOT NULL,
	review text NULL,
	CONSTRAINT reviews_pk PRIMARY KEY (review_id),
	CONSTRAINT reviews_markets_fk FOREIGN KEY (market_id) REFERENCES markets(market_id),
	CONSTRAINT reviews_users_fk FOREIGN KEY (user_id) REFERENCES users(user_id)
);


Inserting into the table
------------------------

INSERT INTO users VALUES(1, 'Konstantin', 'Kuzmin', 'kkuzmin', '827ccb0eea8a706c4c34a16891f84e7b');
INSERT INTO users VALUES(2, 'Wes', 'Turner', 'wturner', 'ee23cd19091ba88bc3cf974d9a5c66ca');


Loading from CSV into the table
------------------------

COPY states
FROM 'c:\RPI\Courses\rcos-s24\RDBMS\ETL\states.csv'
DELIMITER ','
CSV HEADER;

COPY cities
FROM 'c:\RPI\Courses\rcos-s24\RDBMS\ETL\cities.csv'
DELIMITER ','
CSV HEADER;

COPY markets
FROM 'c:\RPI\Courses\rcos-s24\RDBMS\ETL\markets.csv'
DELIMITER ','
CSV HEADER;

COPY categories
FROM 'c:\RPI\Courses\rcos-s24\RDBMS\ETL\categories.csv'
DELIMITER ','
CSV HEADER;

COPY markets_categories
FROM 'c:\RPI\Courses\rcos-s24\RDBMS\ETL\markets_categories.csv'
DELIMITER ','
CSV HEADER;


Creating a read-only user
-------------------------

CREATE ROLE readaccess;
GRANT CONNECT ON DATABASE farmers_markets TO readaccess;
GRANT USAGE ON SCHEMA public TO readaccess;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readaccess;
CREATE USER rcos_student WITH PASSWORD 'abc12345';
GRANT readaccess TO rcos_student;
\c farmers_markets rcos_student


Creating a user for the app
---------------------------
CREATE USER marketsuser WITH PASSWORD '';
ALTER ROLE marketsuser SET client_encoding TO 'utf8';
ALTER ROLE marketsuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE marketsuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE farmers_markets TO marketsuser;
GRANT ALL ON ALL TABLES IN SCHEMA public TO marketsuser;
ALTER DATABASE farmers_markets OWNER TO marketsuser;


Check privileges
----------------
\l
\z




Executing queries
-----------------

SELECT * 
FROM 
  markets m
  , states s
WHERE
  m.state = s.state_id
  AND s.state_abbr = 'NY'
;


SELECT c.category
FROM
  categories c

EXCEPT

SELECT c.category
FROM
  markets m
  JOIN markets_categories mc ON m.market_id = mc.market_id
  JOIN categories c ON mc.category_id = c.category_id
WHERE
  m.market_name LIKE '%Troy Waterfront%'
;

SELECT cit.city, s.state_full, m.market_name
FROM
  cities cit
  JOIN markets m ON cit.city_id = m.city
  JOIN states s ON m.state = s.state_id
  JOIN markets_categories mc ON m.market_id = mc.market_id
  JOIN categories c ON mc.category_id = c.category_id
WHERE
  c.category = 'Crafts'
  AND s.state_abbr in ('NY', 'NJ', 'PA', 'MA', 'VT')
;


INSERT INTO markets_categories
VALUES (102002, 33);

DELETE FROM states s WHERE s.state_abbr = 'NY';

UPDATE users SET password_hash = 'abcdef' WHERE username = 'kkuzmin';


Creating a data-centric application
===================================

https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04
https://www.enterprisedb.com/postgres-tutorials/how-use-postgresql-django
https://djangoadventures.com/how-to-integrate-django-with-existing-database/
https://dev.to/idrisrampurawala/creating-django-models-of-an-existing-db-288m
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Home_page

- Create new Django Project
- Edit settings.py
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'farmers_markets',
          'USER': 'marketsuser',
          'PASSWORD': 'Pa$$W0rd',
          'HOST': 'localhost',
          'PORT': '',
      }
  }

  ALLOWED_HOSTS = ['localhost']
- makemigrations
- migrate
- createsuperuser
  Username: admin
  Password: nimda
- http://localhost:8000/
- http://localhost:8000/admin
- startapp markets
- python manage.py dbshell
- python manage.py inspectdb > models.py
- convert models.py to UTF-8
- migrate --fake-initial


Serverless RDBS
===============
SQLite


NoSQL Database Systems
======================
Neo4j Graph Database: https://neo4j.com/deployment-center/



