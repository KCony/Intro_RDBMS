import psycopg


conn = psycopg.connect(dbname="imdb",
                        host="localhost",
                        user="",
                        password="",
                        port="5432")

cur = conn.cursor()

cur.execute("""SELECT DISTINCT
   a1.name, a1.surname
FROM
   actors a
   , movieroles mr   --- movies with KB
   , movieroles mr1  -- actors in movies for mr1
   , actors a1
WHERE
   a.id = mr.actorid
   and a.name = 'Kevin (I)'
   and a.surname = 'Bacon' 
   and mr1.movieid = mr.movieid
   and mr1.actorid = a1.id
   and mr1.actorid <> a.id ;""")
res = cur.fetchall()
for record in res:
    print(' '.join([str(x) for x in record]))
