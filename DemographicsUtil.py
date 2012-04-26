import csv
import traceback

import sys, os,traceback

#class DemographicsUtil:

def printHelp(nput):
  print nput + " Help!!Help!!"

def getDemographicsText(data,lang):
    transDict = {}
    f = open('translations_text.csv','r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 2:
        transDict[str(text[0])] = text[1]
      else:
        transDict[str(text[0])] = text[2]
    #print transDict
    sch_txt_str=transDict['1'] + transDict['2'] #+ transDict['3']
    presch_txt_str=transDict['2']
    enrol_txt_str= ''
    lang_txt_str = transDict['2']
    neighbours_txt_str ='<br/><br/>' + transDict['29']
    
    #School Text
    if int(data["inst_counts"]["schcount"]) > 0:
      for key in data["cat_sch_tb"]:
        sch_txt_str = ' ' + sch_txt_str + str(data["cat_sch_tb"][key]) + transDict[key.upper()] + ', '
      sch_txt_str = sch_txt_str.rstrip(', ') + transDict['8'] + ' '
      sch_txt_str = sch_txt_str + str(data["inst_counts"]["schcount"]) + transDict['24'] + str(data['gend_sch_tb']['Boy'] + data['gend_sch_tb']['Girl']) + transDict['25'] + transDict['10']
      for key in data['enrol_sch_tb']:
        sch_txt_str = sch_txt_str  + transDict['IN ' + key.upper()] + data['enrol_sch_tb'][key] + ', '
      sch_txt_str = sch_txt_str.rstrip(', ') + transDict['11']
      data['sch_txt'] = sch_txt_str

      for key in data["moi_sch_tb"]:
        lang_txt_str = ' ' + lang_txt_str + str(data["moi_sch_tb"][key]) + transDict[key.upper() + ' MEDIUM'] + ', '
      lang_txt_str = lang_txt_str.rstrip(', ') + transDict['23'] + '.'
      trans_list = []
      for i in data['mt_sch_ord_lst']:
        trans_list.append(transDict[i.upper()])
      lang_txt_str = lang_txt_str + transDict['15'] + ', '.join(trans_list) + transDict['16']
      data['lang_txt'] = lang_txt_str

      presch_txt_str = presch_txt_str + data["inst_counts"]["schcount"] + ' ' + transDict['3'] + str(data['gend_sch_tb']['Boy']) + transDict['4'] + str(data['gend_sch_tb']['Girl']) + transDict['5']
      
    #Preschool Text
    if int(data["inst_counts"]["preschcount"]) > 0:
      presch_txt_str = presch_txt_str + data["inst_counts"]["preschcount"] + ' ' + transDict['9'] + str(data['gend_presch_tb']['Boy']) + transDict['4'] + str(data['gend_presch_tb']['Girl']) + transDict['5']
      data['presch_txt'] = presch_txt_str
      
      enrol_txt_str = enrol_txt_str + transDict['22'] + str(data["inst_counts"]["preschcount"]) + transDict['26'] + str(data['gend_presch_tb']['Boy'] + data['gend_presch_tb']['Girl']) + transDict['25'] + transDict['12']
      for key in data['enrol_presch_tb']:
        enrol_txt_str = '<br/><br/>' + enrol_txt_str + data['enrol_presch_tb'][key]
      enrol_txt_str = enrol_txt_str + transDict['13'] + '<br/><br/>'
      enrol_txt_str = enrol_txt_str + transDict['17'] + ', '.join(data['mt_presch_ord_lst']) + transDict['16'] + transDict['18']
      data['enrol_txt'] = enrol_txt_str
    else:
      data['presch_txt'] =presch_txt_str #+ '<br/><br/>' + transDict['29'] 
      data['enrol_txt'] ='<br/><br/>' + transDict['29']


    #Neighbours Text
    if 'neighbours_sch_hasdata' not in data.keys():
      choice = 'neighbours_sch'
      if len(data['neighbours_presch'].keys()) > len(data['neighbours_sch'].keys()):
        choice = 'neighbours_presch'
      neighbours = data[choice].keys()
      neighbours.remove(data['const_name'])
      neighbours_txt_str = '<br/><br/>' + data['const_name'] + ' ' + transDict['19'] + ', '.join(neighbours) + '. ' + transDict['20']
    data['neighbours_txt'] = neighbours_txt_str + transDict['21'] + transDict['27']
    return data


