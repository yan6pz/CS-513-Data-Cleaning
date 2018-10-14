select name,lat,long,dated,personal,family,quant,reading from site s
 inner join visited v on v.site==s.name
 inner join survey su on su.taken == v.id
  inner join person p on su.person =p.id
  where dated is not null
  order by dated, personal, family, quant, reading