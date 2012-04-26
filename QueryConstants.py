common_queries = {
'get_mp_const':"select const_ward_name,id from tb_electedrep_master where parent=4 and const_ward_type='MP Constituency' and status='active' order by const_ward_name;",
'get_mla_const':"select const_ward_name,id from tb_electedrep_master where parent in (4,5) and const_ward_type='MLA Constituency' and status='active' order by const_ward_name;",
}

mla_queries = {
'mla_gend_sch':"select tssc.sex, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=1 group by tssc.sex",
'mla_gend_presch':"select tssc.sex, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.sex",
'mla_mt_sch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=1 group by tssc.mt;",
'mla_mt_presch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.mt;",
'mla_schcount':"select count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and tse.heirarchy=1;",
'mla_preschcount':"select count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and tse.heirarchy=2 and tssc.sid=tse.sid and tssc.cat='Anganwadi';",
'mla_const_details':"select elec_comm_code, const_ward_name , current_elected_rep, const_ward_type, neighbours,current_elected_party from tb_electedrep_master where const_ward_type='MLA Constituency' and id=%s;",
'mla_moi_sch':"select distinct tssc.moi, count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=1 group by tssc.moi;",
#'mla_moi_presch':"select distinct tssc.moi, count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.moi;",
'mla_cat_sch':"select distinct tssc.cat, count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=1 group by tssc.cat;",
'mla_cat_presch':"select distinct tssc.cat, count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.cat;",
'mla_neighbour_sch':"select distinct tem.const_ward_name,count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse, tb_electedrep_master tem where tse.mla_const_id = tem.id and tse.sid=tssc.sid and tem.elec_comm_code in %s and tse.heirarchy=1 group by tem.const_ward_name;",
'mla_neighbour_presch':"select distinct tem.const_ward_name,count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse, tb_electedrep_master tem where tse.mla_const_id = tem.id and tse.sid=tssc.sid and tem.elec_comm_code in %s and tse.heirarchy=2 and tssc.cat='Anganwadi' group by tem.const_ward_name;",
'mla_neighbour_gendsch':"select distinct tem.const_ward_name, tssc.sex, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=tssc.sid and tse.mla_const_id = tem.id and tem.elec_comm_code in %s and heirarchy=1 group by tem.const_ward_name,tssc.sex",
'mla_neighbour_gendpresch':"select distinct tem.const_ward_name, tssc.sex, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=tssc.sid and tse.mla_const_id = tem.id and tem.elec_comm_code in %s and heirarchy=2 and tssc.cat='Anganwadi' group by tem.const_ward_name,tssc.sex",
'mla_enrol_sch':"select distinct tssc.cat, sum(tssc.numstu)/count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=1 group by tssc.cat;",
'mla_enrol_presch':"select distinct tssc.cat, sum(tssc.numstu)/count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mla_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.cat;",
'mla_tlmgrant_sch':"select tem.const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(vdf.teacher_count) as total_grant from tb_electedrep_master tem,tb_school_electedrep tse, vw_paisa_data vpd, vw_school_dise vsd, vw_dise_facility vdf where tem.id=tse.mla_const_id and tse.sid=vsd.sid and vdf.dise_id=vsd.dise_code and vpd.criteria='teacher_count' and tse.mla_const_id=%s group by tem.const_ward_name, vpd.grant_type, vpd.grant_amount;",
'mla_mtncgrant_sch':"select tem.const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, count(distinct tse.sid), vpd2.grant_amount * count(distinct tse.sid) as total_grant from (select vdf.dise_id as dise_id, CASE WHEN vdf.classroom_count <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator from vw_paisa_data vpd, vw_dise_facility vdf where vpd.criteria='classroom_count') AS mvdf, tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd2 where tem.id=tse.mla_const_id and tse.sid = vsd.sid and mvdf.dise_id=vsd.dise_code and mvdf.operator = vpd2.operator and tse.mla_const_id=%s group by tem.const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by tem.const_ward_name;",
'mla_annualgrant_sch':"select tem.const_ward_name, vsd.cat, vpd.grant_type, count(distinct tse.sid), vpd.grant_amount * count(distinct tse.sid) as total_grant from tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd where tem.id=tse.mla_const_id and tse.sid=vsd.sid and vpd.criteria='school_cat' and vpd.factor = vsd.cat::text and tse.mla_const_id=%s group by tem.const_ward_name, vsd.cat,vpd.grant_type,vpd.grant_amount order by tem.const_ward_name, vsd.cat;",
'mla_neighbor_annual':"select tem.const_ward_name, vsd.cat, vpd.grant_type, vpd.grant_amount * count(distinct tse.sid) as total_grant from tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd where tem.id=tse.mla_const_id and tse.sid=vsd.sid and vpd.criteria='school_cat' and vpd.factor = vsd.cat::text and tem.elec_comm_code in %s group by tem.const_ward_name, vsd.cat,vpd.grant_type,vpd.grant_amount order by tem.const_ward_name, vsd.cat;",
'mla_neighbor_tlm':"select tem.const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(vdf.teacher_count) as total_grant from tb_electedrep_master tem,tb_school_electedrep tse, vw_paisa_data vpd, vw_school_dise vsd, vw_dise_facility vdf where tem.id=tse.mla_const_id and tse.sid=vsd.sid and vdf.dise_id=vsd.dise_code and vpd.criteria='teacher_count' and tem.elec_comm_code in %s  group by tem.const_ward_name, vpd.grant_type, vpd.grant_amount;",
'mla_neighbor_mntnc':"select tem.const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, vpd2.grant_amount * count(distinct tse.sid) as total_grant from (select vdf.dise_id as dise_id, CASE WHEN vdf.classroom_count <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator from vw_paisa_data vpd, vw_dise_facility vdf where vpd.criteria='classroom_count') AS mvdf, tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd2 where tem.id=tse.mla_const_id and tse.sid = vsd.sid and mvdf.dise_id=vsd.dise_code and mvdf.operator = vpd2.operator and tem.elec_comm_code in %s group by tem.const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by tem.const_ward_name;",
'mla_abs_schcount':'select count(distinct tse.sid) from tb_school_electedrep tse where tse.mla_const_id=%s and tse.heirarchy=1;',
'mla_abs_preschcount':'select count(distinct tse.sid) from tb_school_electedrep tse where tse.mla_const_id=%s and tse.heirarchy=2;',
'mla_fin_schcount':'select count(distinct tse.sid) from vw_school_dise vsd, tb_school_electedrep tse where vsd.sid=tse.sid and tse.mla_const_id=%s and tse.heirarchy=1;',
}

mp_queries = {
'mp_gend_sch':"select tssc.sex, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=1 group by tssc.sex",
'mp_gend_presch':"select tssc.sex, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.sex",
'mp_mt_sch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=1 group by tssc.mt;",
'mp_mt_presch':"select tssc.mt, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.mt;",
'mp_schcount':"select count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and tse.heirarchy=1;",
'mp_preschcount':"select count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and tse.heirarchy=2 and tssc.cat='Anganwadi';",
'mp_const_details':"select elec_comm_code, const_ward_name , current_elected_rep, const_ward_type, neighbours, current_elected_party from tb_electedrep_master where const_ward_type='MP Constituency' and id=%s;",
'mp_moi_sch':"select distinct tssc.moi, count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=1 group by tssc.moi;",
#'mp_moi_presch':"select distinct tssc.moi, count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.moi;",
'mp_cat_sch':"select distinct tssc.cat, count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=1 group by tssc.cat;",
'mp_cat_presch':"select distinct tssc.cat, count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.cat;",
'mp_neighbour_sch':"select distinct tem.const_ward_name,count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse, tb_electedrep_master tem where tse.mp_const_id = tem.id and tse.sid=tssc.sid and tem.elec_comm_code in %s and tse.heirarchy=1 group by tem.const_ward_name;",
'mp_neighbour_presch':"select distinct tem.const_ward_name,count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse, tb_electedrep_master tem where tse.mp_const_id = tem.id and tse.sid=tssc.sid and tem.elec_comm_code in %s and tse.heirarchy=2 and tssc.cat='Anganwadi' group by tem.const_ward_name;",
'mp_neighbour_gendsch':"select distinct tem.const_ward_name, tssc.sex, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=tssc.sid and tse.mp_const_id = tem.id and tem.elec_comm_code in %s and heirarchy=1 group by tem.const_ward_name,tssc.sex",
'mp_neighbour_gendpresch':"select distinct tem.const_ward_name, tssc.sex, sum(tssc.numstu) from tb_school_stu_counts tssc, tb_school_electedrep tse,tb_electedrep_master tem where tse.sid=tssc.sid and tse.mp_const_id = tem.id and tem.elec_comm_code in %s and heirarchy=2 and tssc.cat='Anganwadi' group by tem.const_ward_name,tssc.sex",
'mp_enrol_sch':"select distinct tssc.cat, sum(tssc.numstu)/count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=1 group by tssc.cat;",
'mp_enrol_presch':"select distinct tssc.cat, sum(tssc.numstu)/count(distinct tssc.sid) from tb_school_stu_counts tssc, tb_school_electedrep tse where tse.sid=tssc.sid and tse.mp_const_id=%s and heirarchy=2 and tssc.cat='Anganwadi' group by tssc.cat;",
'mp_tlmgrant_sch':"select tem.const_ward_name, vpd.grant_type,vpd.grant_amount,vpd.grant_amount* sum(vdf.teacher_count) as total_grant from tb_electedrep_master tem,tb_school_electedrep tse, vw_paisa_data vpd, vw_school_dise vsd, vw_dise_facility vdf where tem.id=tse.mp_const_id and tse.sid=vsd.sid and vdf.dise_id=vsd.dise_code and vpd.criteria='teacher_count' and tse.mp_const_id=%s group by tem.const_ward_name, vpd.grant_type, vpd.grant_amount;",
'mp_mtncgrant_sch':"select tem.const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count,count(distinct tse.sid), vpd2.grant_amount * count(distinct tse.sid) as total_grant from (select vdf.dise_id as dise_id, CASE WHEN vdf.classroom_count <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator from vw_paisa_data vpd, vw_dise_facility vdf where vpd.criteria='classroom_count') AS mvdf, tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd2 where tem.id=tse.mp_const_id and tse.sid = vsd.sid and mvdf.dise_id=vsd.dise_code and mvdf.operator = vpd2.operator and tse.mp_const_id=%s group by tem.const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by tem.const_ward_name;",
'mp_annualgrant_sch':"select tem.const_ward_name, vsd.cat, vpd.grant_type, count(distinct tse.sid), vpd.grant_amount * count(distinct tse.sid) as total_grant from tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd where tem.id=tse.mp_const_id and tse.sid=vsd.sid and vpd.criteria='school_cat' and vpd.factor = vsd.cat::text and tse.mp_const_id=%s group by tem.const_ward_name, vsd.cat,vpd.grant_type,vpd.grant_amount order by tem.const_ward_name, vsd.cat;",
'mp_neighbor_annual':"select tem.const_ward_name, vsd.cat, vpd.grant_type, vpd.grant_amount * count(distinct tse.sid) as total_grant from tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd where tem.id=tse.mp_const_id and tse.sid=vsd.sid and vpd.criteria='school_cat' and vpd.factor = vsd.cat::text and tem.elec_comm_code in %s group by tem.const_ward_name, vsd.cat,vpd.grant_type,vpd.grant_amount order by tem.const_ward_name, vsd.cat;",
'mp_neighbor_tlm':"select tem.const_ward_name, vpd.grant_type, vpd.grant_amount, vpd.grant_amount* sum(vdf.teacher_count) as total_grant from tb_electedrep_master tem,tb_school_electedrep tse, vw_paisa_data vpd, vw_school_dise vsd, vw_dise_facility vdf where tem.id=tse.mp_const_id and tse.sid=vsd.sid and vdf.dise_id=vsd.dise_code and vpd.criteria='teacher_count' and tem.elec_comm_code in %s  group by tem.const_ward_name, vpd.grant_type, vpd.grant_amount;",
'mp_neighbor_mntnc':"select tem.const_ward_name, vpd2.grant_type, CASE WHEN mvdf.operator='gt' THEN 'With more than 3 classrooms ' ELSE 'With 3 classrooms or fewer ' END as classroom_count, vpd2.grant_amount * count(distinct tse.sid) as total_grant from (select vdf.dise_id as dise_id, CASE WHEN vdf.classroom_count <= CAST (vpd.factor AS INT) THEN 'lt' ELSE 'gt' END as operator from vw_paisa_data vpd, vw_dise_facility vdf where vpd.criteria='classroom_count') AS mvdf, tb_electedrep_master tem, tb_school_electedrep tse, vw_school_dise vsd, vw_paisa_data vpd2 where tem.id=tse.mp_const_id and tse.sid = vsd.sid and mvdf.dise_id=vsd.dise_code and mvdf.operator = vpd2.operator and tem.elec_comm_code in %s group by tem.const_ward_name, vpd2.grant_type, mvdf.operator, vpd2.grant_amount order by tem.const_ward_name;",
'mp_abs_schcount':'select count(distinct tse.sid) from tb_school_electedrep tse where tse.mp_const_id=%s and tse.heirarchy=1;',
'mp_abs_preschcount':'select count(distinct tse.sid) from tb_school_electedrep tse where tse.mp_const_id=%s and tse.heirarchy=2;',
'mp_fin_schcount':'select count(distinct tse.sid) from vw_school_dise vsd, tb_school_electedrep tse where vsd.sid=tse.sid and tse.mp_const_id=%s and tse.heirarchy=1;',
}


def getDictionary(constype = 'common'):
  if constype == 'mp':
    return mp_queries
  elif constype == 'mla':
    return mla_queries
  else:
    return common_queries
