import csv
import traceback

import sys, os,traceback

#class DemographicsUtil:

def printHelp(nput):
  print nput + " Help!!Help!!"

def getFinancesText(data,lang):
    transDict = {}
    f = open('fin_translations_text.csv','r')
    for line in f.readlines():
      text = line.split('|')
      if lang == 2:
        transDict[str(text[0])] = text[1]
      else:
        transDict[str(text[0])] = text[2]
    intro_txt_str=transDict['1'] + transDict['18'] 
    summary_txt_str=transDict['17']
    annual_txt_str=transDict['17']
    mtnc_txt_str=transDict['17']
    tlm_txt_str=transDict['17']
    neighbours_txt_str=transDict['17']
    
    #School Text
    if int(data["inst_counts"]["abs_schcount"]) > 0:
      data['intro_txt'] = intro_txt_str 
      #--------------------- SUMMARY 
      total_grant = data["total_tlm"] + data["total_annual"] + data["total_mntc"]
      summary_txt_str = transDict['24'] + formatIndian(total_grant) + '. ' + transDict['25'] + formatIndian(data["total_tlm"]) + '. '
      summary_txt_str = summary_txt_str + transDict['26'] + formatIndian(data["total_annual"]) + '. ' + transDict['27'] + formatIndian(data["total_mntc"]) + '. '
      data['summary_txt'] = summary_txt_str 
      #---------------------- TLM
      tlm_txt_str = transDict['19'] + str(data['tlmgrant_sch']['teacher_count']) + transDict['20'] + formatIndian(data["total_tlm"]) + transDict['8'] + '. '
      data['tlm_txt'] = tlm_txt_str
      #---------------------- Annual
      annual_txt_str = transDict['23'] 
      totalsg =  0
      for key in data["annualgrant_sch"]:
        annual_txt_str = ' ' + annual_txt_str + transDict[key.upper()] + formatIndian(data["annualgrant_sch"][key][1]) + ', '
        totalsg = totalsg + int(data["annualgrant_sch"][key][0])
      annual_txt_str = annual_txt_str.rstrip(', ') + transDict['8'] + '. '
      annual_txt_str = annual_txt_str + transDict['30'] + str(totalsg) + transDict['31']
      data['annual_txt'] = annual_txt_str
      #---------------------- Maintenance
      mtnc_txt_str = transDict['21']  + formatIndian(data["mtncgrant_sch"]["With 3 classrooms or fewer "][1]) 
      mtnc_txt_str = mtnc_txt_str + transDict['22'] + formatIndian(data["mtncgrant_sch"]["With more than 3 classrooms "][1]) + transDict['8'] + '. '
      mtnc_txt_str = mtnc_txt_str + transDict['28'] + str(int(data["mtncgrant_sch"]["With 3 classrooms or fewer "][0]) + int(data["mtncgrant_sch"]["With more than 3 classrooms "][0]))
      mtnc_txt_str = mtnc_txt_str +'/'+str(totalsg)+ transDict['29']
      data['mtnc_txt'] = mtnc_txt_str
  
      #---------------------- Neighbours
      neighbours = data["neighbours_grant"].keys()
      if neighbours:
        neighbours.remove(data['const_name'])
        neighbours_txt_str = '' + data['const_name'] + ' ' + transDict['11'] + ', '.join(neighbours) + '. ' + transDict['12']
      data['neighbours_txt'] = neighbours_txt_str + transDict['15']
    
      data['source_txt'] = transDict['16']
    return data

def formatIndian(inputNum) :
  prefStr = ''
  outputString = ''
  minus = ''
  suf = ''
  lastThree = ''
  try:
    inputString = str(inputNum)
    if '.' in inputString:
      numberArray = inputString.split('.', 2)
      pref = int(numberArray[0])
      suf = numberArray[1]
    else:
      pref = inputString
      suf = ''
    outputString = ''
    minus = ''
    if pref < 0:
      minus = '-'
    prefStr = str(pref)
    if len(prefStr) > 3 :
      lastThree = prefStr[len(prefStr)-3: len(prefStr)]
      prefStr = prefStr[0: len(prefStr)-3]
    if len(prefStr) % 2 > 0 :
      outputString = outputString + prefStr[0:1] + ','
      prefStr = prefStr[1: len(prefStr)]

    while (len(prefStr) >= 2) :
      outputString = outputString +  prefStr[0:2] + ','
      prefStr = prefStr[2:len(prefStr)]

    outputString = minus + outputString +  lastThree + suf
    return outputString
  except:
    print 'Error occurred'
    print "Unexpected error:", sys.exc_info()
    traceback.print_exc(file=sys.stdout)
    return 'NaN'
