select distinct p1.pid,p1.authors,p1.year,p1.title,p1.journal,p1.vol,p1.no,p1.fp,p1.lp,p1.publisher
 from publication as p1,publication as p2 where p1.pid==p2.pid and p1.lp<p2.fp;