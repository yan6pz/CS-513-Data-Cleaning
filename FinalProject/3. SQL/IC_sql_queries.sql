/*latitude and longitude should be in the interval [0,90], [-180,180]   */ 
SELECT m.fmid, 
       m.marketname, 
       m.x, 
       m.y 
FROM   markets m 
WHERE  ( Cast(m.x AS FLOAT) > 180 
          OR Cast(m.x AS FLOAT) <- 180 
          OR Cast(m.y AS FLOAT) < 0 
          OR Cast(m.y AS FLOAT) > 90 ) 
        OR ( m.x IS NULL 
              OR m.y IS NULL 
              OR m.x = '' 
              OR m.y = '' ); 

/*There are no inactive markets. There should be at least one datetime per market in seasondates. And the datefrom and dateto values should not be empty  */
SELECT m.fmid, 
       m.marketname, 
       sd.datefrom, 
       sd.dateto 
FROM   markets m 
       left join seasondates sd 
              ON sd.id == m.fmid 
WHERE  sd.datefrom IS NULL 
        OR sd.dateto IS NULL 
        OR sd.datefrom = '' 
        OR sd.dateto = ''; 

/*Select all the markets that have seafood and vegetables and are opened in November    */ 
SELECT m.fmid, 
       m.marketname, 
       dates.datefrom, 
       dates.dateto 
FROM   markets m, 
       (SELECT Strftime('%m', sa.datefrom) AS datefrom, 
               Strftime('%m', sa.dateto)   AS dateto, 
               m1.fmid 
        FROM   markets m1 
               inner join seasondates sa 
                       ON m1.fmid = sa.id 
        WHERE  m1.seafood = 'Y' 
               AND m1.vegetables = 'Y') dates 
WHERE  dates.fmid = m.fmid 
       AND ( dates.datefrom = '11' 
              OR dateto = '11' ); 

/*There should not be two markets that are in the same location during the same time   */ 
SELECT * 
FROM   (SELECT m.fmid, 
               m.zip, 
               m.street, 
               s.name  AS state, 
               co.name AS county, 
               c.name  AS city, 
               sd.datefrom 
        FROM   markets AS m 
               inner join cities c 
                       ON m.city = c.cityid 
               inner join counties co 
                       ON m.county = co.countyid 
               inner join states s 
                       ON m.state = s.stateid 
               inner join seasondates sd 
                       ON m.fmid = sd.id) AS m, 
       (SELECT m1.fmid     AS fmid1, 
               m1.zip      AS zip1, 
               m1.street   AS street1, 
               s.name      AS state1, 
               co.name     AS county1, 
               c.name      AS city1, 
               sd.datefrom AS datefrom1 
        FROM   markets AS m1 
               inner join cities c 
                       ON m1.city = c.cityid 
               inner join counties co 
                       ON m1.county = co.countyid 
               inner join states s 
                       ON m1.state = s.stateid 
               inner join seasondates sd 
                       ON m1.fmid = sd.id) AS m1 
WHERE  m1.zip1 = m.zip 
       AND m1.county1 = m.county 
       AND m1.city1 = m.city 
       AND m1.street1 = m.street 
       AND m1.state1 = m.state 
       AND m1.datefrom1 = m.datefrom 
       AND m1.fmid1 <> m.fmid; 

/*All the markets should have non-empty city, state and county  */ 
SELECT m.fmid, 
       m.marketname, 
       c.name  AS 'city', 
       s.name  AS 'state', 
       co.name AS 'county' 
FROM   markets m 
       inner join cities c 
               ON m.city = c.cityid 
       inner join counties co 
               ON m.county = co.countyid 
       inner join states s 
               ON m.state = s.stateid 
WHERE  ( c.name IS NULL 
          OR c.name = '' ) 
        OR ( co.name IS NULL 
              OR co.name = '' ) 
        OR ( s.name IS NULL 
              OR s.name = '' ); 

/*No empty names for cities, states, counties   */ 
SELECT * 
FROM   states s 
WHERE  s.name IS NULL 
        OR s.name = ''; 

SELECT * 
FROM   counties c 
WHERE  c.name IS NULL 
        OR c.name = ''; 

SELECT * 
FROM   cities c 
WHERE  c.name IS NULL 
        OR c.name = ''; 