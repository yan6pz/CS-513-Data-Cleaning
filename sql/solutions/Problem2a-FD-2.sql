select t.journal, t.publisher from (
select  distinct p1.publisher,p1.journal
 from publication as p1,publication as p2 where p1.journal==p2.journal
 and (p1.publisher!=p2.publisher or( p1.publisher is null and p2.publisher is not null) or( p1.publisher is not null and p2.publisher is null))) t;