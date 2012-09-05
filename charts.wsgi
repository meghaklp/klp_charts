import web
import psycopg2
import decimal
import jsonpickle
import csv
import re
from web import form
import datetime
import traceback
import simplejson
import codecs
from operator import itemgetter
import ho.pisa as pisa

# Needed to find the templates
import sys, os,traceback
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import Utility.KLPDB
import QueryConstants
import DemographicsUtil
import FinancesUtil
import InfraUtil

connection = Utility.KLPDB.getConnection()
cursor = connection.cursor()
render = web.template.render('templates/')

urls = (
     '/charts/(.*)/(.*)/(.*)/(.*)','Charts',
     '/demographics','Demographics',
     '/finances','Finances',
     '/infrastructure','Infrastructure',
)

application = web.application(urls,globals()).wsgifunc()

class Charts:
  
  """Returns the main template"""
  def GET(self,searchby,constid,rep_lang,rep_type):
    if searchby =='1':
      constype = 1
    else:
      constype = 2
    lang = 2
    if rep_lang=='1':
      lang = 1
    data = {}
    util = CommonUtil()
    print str(searchby) + ' ' +  str(constid) + ' ' + str(rep_lang) + ' ' + str(rep_type) 
    if rep_type == '1':
      demographics = Demographics()
      queries = ['schcount','preschcount']
      data.update(util.countsTable(constype,[constid],queries))
      data.update(demographics.generateData(constype,[constid]))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(DemographicsUtil.getDemographicsText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.demographics(simplejson.dumps(data,sort_keys=True))
    elif rep_type == '2':
      finances = Finances()
      queries = ['abs_schcount','fin_schcount']
      data.update(util.countsTable(constype,[constid],queries))
      data.update(finances.generateData(constype,[constid]))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(FinancesUtil.getFinancesText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.finances(simplejson.dumps(data,sort_keys=True))
    elif rep_type == '3':
      infra = Infrastructure()
      queries = ['abs_schcount','abs_preschcount']
      data.update(util.countsTable(constype,[constid],queries))
      data.update(infra.generateData(constype,[constid]))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(InfraUtil.getInfraText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.infrastructure(simplejson.dumps(data,sort_keys=True))
    else:
      pass

class Infrastructure:

  def generateData(self,cons_type, constid):
    data = {}
    avgdata = {}
    avgdata = self.getAverages()

    if cons_type == 1:
      data["const_type"]='MP'
      constype = "mp"
    else:
      data["const_type"]='MLA'
      constype = "mla"
    data["const_name"]=str(constid[0])

    data.update(self.constituencyData(constype,constid))
    data.update(self.getAngInfra(constype,constid,avgdata))
    data.update(self.getSchoolInfra(constype,constid,avgdata))
    print data.keys()
    #data.update(self.getLibInfra(constype,constid))
    return data

  def getAverages(self):
    data = {}
    querykeys = ['get_dise_count_blore','get_sch_count_blore','get_ai_count_blore','get_ang_count_blore']
    for key in querykeys:
      cursor.execute(QueryConstants.getDictionary("common_queries")[key])
      result = cursor.fetchall()
      for row in result:
        data[key.replace("get_","")] = row[0]
      connection.commit()
    querykeys = ['get_dise_avg_blore','get_ai_avg_blore']
    for key in querykeys:
      tabledata = {}
      cursor.execute(QueryConstants.getDictionary("common_queries")[key])
      result = cursor.fetchall()
      for row in result:
        if 'dise' in key:
          tabledata[row[0]] = str(int(row[1]) * 100/int(data['dise_count_blore']))
        else:
          tabledata[row[0]] = str(int(row[1]) * 100/int(data['ai_count_blore']))
      data[key.replace("get_","")] = tabledata
      connection.commit()
    return data

  def getAngInfra(self,constype,constid,data):
    tabledata = {}
    
    blore_count = data['ai_count_blore']
    blore_infra = data['ai_avg_blore']

    querykey = 'infra_count'
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
     infra_count = row[0]
    data[querykey] = infra_count
    connection.commit()

    querykey = 'ang_infra' 
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      if row[0] in ['waste_basket','toilet','toilet_roof','akshara_kits']:
        pass
      else:
        if row[2] in tabledata:
          tabledata[row[2]][row[0]]=[str(int(row[1])*100/int(infra_count)),str(blore_infra[row[0]])]
        else:
          tabledata[row[2]] = {row[0]:[str(int(row[1])*100/int(infra_count)),str(blore_infra[row[0]])]}
    data[querykey] = tabledata
    connection.commit()
    return data

  def getSchoolInfra(self,constype,constid,data):
    tabledata = {}

    blore_count = data['dise_count_blore']
    blore_dise = data['dise_avg_blore']

    querykey = 'dise_count'
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
     dise_count = row[0]
    data[querykey] = dise_count
    connection.commit()

    querykey = 'dise_facility' 
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      if row[0] in ['toilet_all']:
        pass
      else:
        if row[2] in tabledata:
          tabledata[row[2]][row[0]]=[str(int(row[1])*100/int(dise_count)),str(blore_dise[row[0]])]
        else:
          tabledata[row[2]] = {row[0]:[str(int(row[1])*100/int(dise_count)),str(blore_dise[row[0]])]}
    data[querykey] = tabledata
    connection.commit()
    return data

  def getLibInfra(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'lib_count' 
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      lib_count = row[0]
    data[querykey] = lib_count
    connection.commit()
    querykey = 'lib_status' 
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      tabledata[row[0]] = row[1]
    data[querykey] = tabledata
    connection.commit()
    tabledata = {}
    querykey = 'lib_summary' 
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      tabledata['total_books'] = row[0]
      tabledata['total_racks'] = row[1]
      tabledata['total_tables'] = row[2]
      tabledata['total_chairs'] = row[3]
      tabledata['total_comps'] = row[4]
      tabledata['total_ups'] = row[5]
    data[querykey] = tabledata
    connection.commit()
    return data

  def neighboursData(self, neighbours, constype, constid):
    data = {}
    constype_str = constype
    try:
      querykey = 'neighbours_df_count'
      cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],[tuple(neighbours)])
      result = cursor.fetchall()
      dise_count = {} 
      for row in result:
        dise_count[row[0]] = int(row[1])
      data[querykey] = dise_count
      connection.commit()

      querykey = 'neighbours_ai_count'
      cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],[tuple(neighbours)])
      result = cursor.fetchall()
      infra_count = {} 
      for row in result:
        infra_count[row[0]] = int(row[1])
      data[querykey] = infra_count
      connection.commit()

      if len(neighbours) > 0:
        crit='neighbours_'
        query_keys = ['dise','anginfra']
        for key in query_keys:
          tabledata = {}
          counts_dict = {}
          if key == 'dise' :
            counts_dict = dise_count
          else:
            counts_dict = infra_count
          cursor.execute(QueryConstants.getDictionary(constype)[constype_str+'_'+crit+key], [tuple(neighbours)])
          result = cursor.fetchall()
          for row in result:
            if row[1] in ['waste_basket','toilet','toilet_roof','akshara_kits','toilet_all']:
              pass
            else:
              if row[0].strip() in tabledata.keys():
                  tabledata[row[0].strip()][row[3] + '|' + row[1]] = int(row[2])*100/counts_dict[row[0].strip()]
              else:
                tabledata[row[0].strip()]={row[3]+'|'+ row[1]:int(row[2])*100/counts_dict[row[0].strip()]}

          newtable = {}

          for tabkey in tabledata.keys():
            moddata = {}
            moddata = tabledata[tabkey]
            for each in moddata.keys():
              if each in newtable.keys():
                newtable[each][tabkey] = moddata[each] 
              else:
                newtable.update({ each:{tabkey:moddata[each]}})
          data[crit+key] = newtable

          connection.commit()

      return data
    except:
      print 'Error occurred'
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()
      return None


  def constituencyData(self,constype,constid):
    data = {}
    util = CommonUtil()
    ret_data = util.constituencyData(constype,constid)
    data.update(ret_data[0])
    neighboursdata  = self.neighboursData(ret_data[1],ret_data[2],constid)
    if neighboursdata:
      data.update(neighboursdata)
    return data

class Finances:

  def generateData(self,cons_type, constid):
    data = {}
    if cons_type == 1:
      data["const_type"]='MP'
      constype = "mp"
    else:
      data["const_type"]='MLA'
      constype = "mla"
    data["const_name"]=str(constid[0])

    data.update(self.constituencyData(constype,constid))
    data.update(self.getTLMGrant(constype,constid))
    data.update(self.getAnnualGrant(constype,constid))
    data.update(self.getMaintenanceGrant(constype,constid))
    return data

  def getTLMGrant(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'tlmgrant_sch' 
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    for row in result:
      tabledata['grant_amount'] = str(row[3])
      tabledata['teacher_count'] = str(int(row[3])/int(row[2]))
    data[querykey] = tabledata
    data['total_tlm']=int(tabledata['grant_amount'])
    connection.commit()
    return data
  
  def getAnnualGrant(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'annualgrant_sch' 
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    total_grant = 0
    for row in result:
      tabledata[row[1]] = [str(row[3]),str(row[4])]
      total_grant = total_grant + int(row[4])
    data[querykey] = tabledata
    data['total_annual'] = total_grant
    connection.commit()
    return data
   
  def getMaintenanceGrant(self,constype,constid):
    data = {}
    tabledata = {}
    querykey = 'mtncgrant_sch' 
    cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
    result = cursor.fetchall()
    total_grant = 0
    for row in result:
      tabledata[row[2]] = [str(row[3]), str(row[4])]
      total_grant = total_grant + int(row[4])
    data[querykey] = tabledata
    data['total_mntc'] = total_grant
    connection.commit()
    return data

  def constituencyData(self,constype,constid):
    data = {}
    util = CommonUtil()
    ret_data = util.constituencyData(constype,constid)
    data.update(ret_data[0])
    data.update(self.neighboursData(ret_data[1],ret_data[2]))
    return data

  def neighboursData(self, neighbours, constype):
    data = {}
    constype_str = constype 
    tabledata = {}
    try:
      if len(neighbours) > 0:
        crit='neighbor_'
        query_keys = ['tlm','annual','mntnc'] 
        for key in query_keys:
          cursor.execute(QueryConstants.getDictionary(constype)[constype_str+'_'+crit+key], [tuple(neighbours)])
          result = cursor.fetchall()
          for row in result:
            if row[0].strip() in tabledata.keys():
              if key in tabledata[row[0].strip()].keys():
                addedup = int(tabledata[row[0].strip()][key]) + int(row[3])
                tabledata[row[0].strip()][key] = addedup
              else:
                tabledata[row[0].strip()][key] = row[3]
            else:
              tabledata[row[0].strip()]={key:row[3]}
      data['neighbours_grant'] = tabledata
      connection.commit()
      return data
    except:
      print 'Error occurred'
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()
      return None

class Demographics:

  def generateData(self,cons_type, constid):
    data = {}
    if cons_type == 1:
      data["const_type"]='MP'
      constype = "mp"
    else:
      data["const_type"]='MLA'
      constype = "mla"
    data["const_name"]=str(constid[0])

    queries = ['gend_sch','gend_presch']
    data.update(self.genderGraphs(constype,constid,queries))
    queries = ['mt_sch','mt_presch']
    data.update(self.mtGraphs(constype,constid,queries))
    queries = ['moi_sch','cat_sch','enrol_sch','enrol_presch']
    data.update(self.pieGraphs(constype,constid,queries))
    data.update(self.constituencyData(constype,constid))
    return data


  def genderGraphs(self,constype,constid,qkeys):
    data = {}
    for querykey in qkeys:
      cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      chartdata ={}
      for row in result:
        chartdata[str(row[0].strip())] = int(row[1])
      if len(chartdata.keys()) > 0:
        total = chartdata['Boy']+chartdata['Girl']
        percBoys = round(float(chartdata['Boy'])/total*100,0)
        percGirls = round(float(chartdata['Girl'])/total*100,0)
        data[querykey+"_tb"]=chartdata
      else:
        data[querykey+"_hasdata"] = 0
      connection.commit()
    return data

  def mtGraphs(self,constype,constid,qkeys):
    data = {}
    for querykey in qkeys:
      cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      tabledata = {}
      invertdata = {}
      order_lst = []
      for row in result:
        invertdata[int(row[1])] = str(row[0].strip().title())
      if len(invertdata.keys()) > 0:
        checklist = sorted(invertdata)
        others = 0
        for i in checklist[0:len(checklist)-4]:
          others = others + i
          del invertdata[i]
        invertdata[others] = 'Others'
        tabledata = dict(zip(invertdata.values(),invertdata.keys()))
        if 'Other' in tabledata.keys():
          tabledata['Others'] = tabledata['Others'] + tabledata['Other']
          del tabledata['Other']
      for i in sorted(tabledata,key=tabledata.get,reverse=True):
        order_lst.append(i)
      if len(tabledata.keys()) > 0:
        data[querykey + "_tb"] = tabledata
        data[querykey + "_ord_lst"] = order_lst 
      else:
        data[querykey + "_hasdata"] = 0
      connection.commit()
    return data

  def pieGraphs(self,constype,constid,qkeys):
    data = {}
    for querykey in qkeys:
      cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey],constid)
      result = cursor.fetchall()
      tabledata = {}
      for row in result:
        tabledata[str(row[0].strip().title())] = str(int(row[1]))
      sorted_x = sorted(tabledata.items(), key=itemgetter(1))
      tabledata = dict(sorted_x)
      if len(tabledata.keys()) > 0:
        data[querykey + "_tb"] = tabledata
      else:
        data[querykey + "_hasdata"] = 0
      connection.commit()
    return data

  def constituencyData(self,constype,constid):
    data = {}
    util = CommonUtil()
    ret_data = util.constituencyData(constype,constid)
    data.update(ret_data[0])
    data.update(self.neighboursData(ret_data[1],ret_data[2]))
    return data


  def neighboursData(self, neighbours, constype):
    data = {}
    constype_str = constype 
    try:
      if len(neighbours) > 0:
        neighbours_sch = {}
        neighbours_presch = {}
        
        cursor.execute(QueryConstants.getDictionary(constype)[constype_str + '_neighbour_sch'], [tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_sch[row[0].strip()]={'schcount':str(row[1])}
        connection.commit()

        cursor.execute(QueryConstants.getDictionary(constype)[constype_str + '_neighbour_presch'], [tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_presch[row[0].strip()] = {'preschcount':str(row[1])}
        connection.commit()
         
        cursor.execute(QueryConstants.getDictionary(constype)[constype_str + '_neighbour_gendsch'],[tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_sch[row[0].strip()][row[1].strip()] = str(row[2])
        connection.commit()
        
        cursor.execute(QueryConstants.getDictionary(constype)[constype_str + '_neighbour_gendpresch'],[tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_presch[row[0].strip()][row[1].strip()] = str(row[2])
        
        if len(neighbours_sch.keys()) > 0: 
          data["neighbours_sch"] = neighbours_sch          
        else:
          data["neighbours_sch_hasdata"] = 0

        if len(neighbours_presch.keys()) > 0: 
          data["neighbours_presch"] = neighbours_presch          
        else:
          data["neighbours_presch_hasdata"] = 0
        
        connection.commit()

      else:
        data["neighbours_sch_hasdata"] = 0
        data["neighbours_presch_hasdata"] = 0

      return data
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()
      return None


      
class CommonUtil:

  def constituencyData(self,constype,constid):
    data = {}
    result = []
    neighbours = []
    constype_str = ''
    try:
      if constype == 'mp':
        constype_str = 'mp'
      else:
        constype_str = 'mla' 
      cursor.execute(QueryConstants.getDictionary(constype)[constype_str + '_const_details'],constid)
      result = cursor.fetchall()
      for row in result:
        data['const_name'] = row[1].strip() if row[1] != None else ''
        data['const_type'] = row[3].strip() if row[3] != None else ''
        data['const_code'] = row[0] if row[0] != None else ''
        data['const_rep'] = row[2].strip() if row[2] != None else ''
        data['const_party'] = row[5].strip() if row[5] != None else ''
        if row[4] != None:
          neighbours = row[4].strip().split('|')
          neighbours.append(row[0])
      connection.commit()
      return [data,neighbours,constype_str]
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()

  def countsTable(self,cons_type,constid,qkeys):
    try:
      if cons_type == 1:
        constype = "mp"
      else:
        constype = "mla"
      data = {}
      tabledata = {}
      for querykey in qkeys:
        cursor.execute(QueryConstants.getDictionary(constype)[constype + '_' + querykey], constid)
        result = cursor.fetchall()
        for row in result:
          tabledata[querykey] = str(row[0])
      data["inst_counts"] =  tabledata
      connection.commit()
      return data
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      connection.rollback()
      return None

  def getTranslations(self, lang):
    transDict = {}
    f = open('translations_heading.csv','r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 1:
        transDict['H' + str(text[0])] = text[2].strip('\n')
      else:
        transDict['H' + str(text[0])] = text[1]
    f = open('translations_dict.csv','r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 1:
        transDict[str(text[0])] = text[1].strip('\n')
      else:
        transDict[str(text[0])] = text[0]
    return transDict
