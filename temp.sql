Maintainence based on number of class rooms

select

TLM for Teachers



Grant based on category

select tem.const_ward_name, vsd.cat, vpd.grant_type, vpd.grant_amount * count(tse.sid) as total_grant from 
tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd where 
tem.id=tse.mp_const_id and tse.sid=vsd.sid and vpd.criteria='school_cat' and vpd.factor = vsd.cat::text
group by tem.const_ward_name, vsd.cat,vpd.grant_type,vpd.grant_amount order by tem.const_ward_name, vsd.cat;

TLM for Teachers

select tem.const_ward_name, vpd.grant_type, vpd.grant_amount* sum(vdf.teacher_count) as total_grant from tb_electedrep_master tem, 
tb_school_electedrep tse, vw_paisa_data vpd, vw_school_dise vsd, vw_dise_facility vdf where tem.id=tse.mp_const_id 
and tse.sid=vsd.sid and vdf.dise_id=vsd.dise_code and vpd.criteria='teacher_count' group by tem.const_ward_name,
vpd.grant_type, vpd.grant_amount;

Maintainence based on number of class rooms

select tem.const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN '> 3 ' ELSE '<= 3 ' END as classroom_count, 
vpd2.grant_amount * count(tse.sid) as total_grant from 
(select vdf.dise_id as dise_id, CASE WHEN vdf.classroom_count <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator
from vw_paisa_data vpd, vw_dise_facility vdf where vpd.criteria='classroom_count') AS mvdf,
tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd2 where tem.id=tse.mp_const_id and
tse.sid = vsd.sid and mvdf.dise_id=vsd.dise_code and mvdf.operator = vpd2.operator 
group by tem.const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by tem.const_ward_name;


