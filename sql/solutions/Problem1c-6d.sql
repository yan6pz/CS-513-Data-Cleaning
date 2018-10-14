
select group_concat(name,',')  from (select (personal || " " || family) as name from Person order by family);