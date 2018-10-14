
select citing, cited,p1.year,p2.year from cites  c
inner join publication p1 on p1.pid==c.citing
inner join publication p2 on p2.pid==c.cited
where p1.year < p2.year