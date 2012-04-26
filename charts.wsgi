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

connection = Utility.KLPDB.getConnection()
cursor = connection.cursor()
render = web.template.render('templates/')

urls = (
     '/charts/(.*)/(.*)/(.*)/(.*)','Charts',
     '/demographics','Demographics',
     '/finances','Finances',
)

application = web.application(urls,globals()).wsgifunc()

class Charts:
  
  """Returns the main template"""
  def GET(self,searchby,constid,rep_lang,rep_type):
#  def GET(self,searchby):
#   return self.makeForm()
  
#  def makeForm(self):
#    web.header('Content-Type','text/html; charset=utf-8')
#
#    cursor.execute(QueryConstants.getDictionary()['get_mp_const'])
#    result = cursor.fetchall()
#    mp_dropdown = []
#    for row in result:
#      if row[0].strip() != '':
#        mp_dropdown.append((row[1],row[0]))

#    cursor.execute(QueryConstants.getDictionary()['get_mla_const'])
#    result = cursor.fetchall()
#    mla_dropdown = []
#    for row in result:
#      if row[0].strip() != '':
#        mla_dropdown.append((row[1],row[0]))

#    self.f =form.Form(
#      form.Radio('searchby',[(1,'MP Only'),(2,'MLA Only')], description="I need a report for a "),
#      form.Radio('rep_lang',[(1,'bilingual report - English & Kannada'),(2,'report in English')], description="I need a "),
#      form.Radio('rep_type',[(1,'Demographics'),(2,'Financial Allocation')], description="based on "),
#      form.Dropdown("mplist", mp_dropdown, description="MP constituency:"),
#      form.Dropdown("mlalist", mla_dropdown, description="MLA constituency:"),
#      form.Button("submit", type="submit", description="Get me the graphs!")
#    )
#    return render.index(self.f)

#  def POST(self): 

#    i = web.input()
#    if i['searchby'][1]=='1':
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
      data.update(demographics.generateData(constype,[constid],lang))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(DemographicsUtil.getDemographicsText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.demographics(simplejson.dumps(data,sort_keys=True))
    elif rep_type == '2':
      finances = Finances()
      queries = ['abs_schcount','fin_schcount']
      data.update(util.countsTable(constype,[constid],queries))
      data.update(finances.generateData(constype,[constid],lang))
      data.update({'transdict':util.getTranslations(lang)})
      data.update(FinancesUtil.getFinancesText(data,lang))
      web.header('Content-Type','text/html; charset=utf-8')
      return render.finances(simplejson.dumps(data,sort_keys=True))
    else:
      #return self.makeForm()
      pass


class Finances:

  def generateData(self,cons_type, constid,lang):
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
      return data
    except:
      print 'Error occurred'
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
      return None

class Demographics:

  def generateData(self,cons_type, constid,lang):
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
        
        cursor.execute(QueryConstants.getDictionary(constype)[constype_str + '_neighbour_presch'], [tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_presch[row[0].strip()] = {'preschcount':str(row[1])}
        
        cursor.execute(QueryConstants.getDictionary(constype)[constype_str + '_neighbour_gendsch'],[tuple(neighbours)])
        result = cursor.fetchall()
        for row in result:
          neighbours_sch[row[0].strip()][row[1].strip()] = str(row[2])
        
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
      else:
        data["neighbours_sch_hasdata"] = 0
        data["neighbours_presch_hasdata"] = 0

      return data
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
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
      return [data,neighbours,constype_str]
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)

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
      data["inst_counts"] = tabledata
      print data
      return data
    except:
      print "Unexpected error:", sys.exc_info()
      traceback.print_exc(file=sys.stdout)
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
