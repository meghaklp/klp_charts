var info;
var translations;

// Load the Visualization API and the piechart package.
google.load('visualization', '1', {'packages':['corechart','table','imagechart']});
var table1;

function sortDict(unsortedObj)
{
var sortable = [];
for (var key in unsortedObj)
    sortable.push([key, unsortedObj[key]]);
var sortedDict = sortable.sort(function(a, b) {return b[1] - a[1]});
return sortedDict;
}

function roundNumber(rnum, rlength) { // Arguments: number to round, number of decimal places
var newnumber = Math.round(rnum*Math.pow(10,rlength))/Math.pow(10,rlength);
return parseFloat(newnumber); // Output the result to the form field (change for your purposes)
}

function isEmpty(ob){
 for(var i in ob){ return false;}
return true;
}

    
function initialise(data)
{

info = data;
translations = info['transdict'];
now = new Date()
document.getElementById("reportdate").innerHTML = now.toDateString();
document.getElementById("rephead").innerHTML = "<img src=\'/images/KLP_logo2.png\' width='130px' vertical-align='top' border=0 />" + '<br/>' + translations['H56'];
document.getElementById("anghead").innerHTML = translations['H78'];
//document.getElementById("libhead").innerHTML = translations['H80'];
document.getElementById("schoolhead").innerHTML = translations['H79'];
//document.getElementById("notehead").innerHTML = translations['H81'];
document.getElementById("neighhead").innerHTML = translations['H40'];

document.getElementById("constname").innerHTML = translations[info["const_type"]] + " <img src=\'../images/arrow.gif\' width='8px' vertical-align='center' border='0'/>" + "<br/><h1>"  
                                               + info['const_name'] + "</h1>";
document.getElementById("constinfo").innerHTML =  "<dl class='header-def'><dt>" + translations['H8'] + "</dt><dd>" + info["const_code"] + "</dd>"
                                              + "<dt>" + translations['H9'] + "</dt><dd>" + info["const_rep"] + "</dd>"
                                              + "<dt>" + translations['H10'] + "</dt><dd>" + info["const_party"] + "</dd></dl>";
document.getElementById("hiddenip").innerHTML = '<input type="hidden" name="const_type" value="'+ info["constype"] + '" />' +
        '<input type="hidden" name="const_id" value="'+ info["const_id"] + '" />' +
        '<input type="hidden" name="forreport" value="'+ info["forreport"] + '" />' +
        '<input type="hidden" name="rep_lang" value="'+ info["rep_lang"] + '" />' ;
document.getElementById('instcounts').innerHTML = '<dl class=\'header-def\'><dt style="font-size:9pt">' + translations['H11'] + '</dt><dd>' + info["inst_counts"]["abs_schcount"] + '<dt style="font-size:9pt">' + translations['H12'] + '</dt><dd>' + info["inst_counts"]["abs_preschcount"] +'</dd></dl>';

if(parseInt(info["inst_counts"]["abs_schcount"]) != 0){

  ang_infra_table();
  dise_facility_table();
  //lib_status_chart();
  //lib_summary_chart();
  neighbours_anginfra();
  neighbours_dise();
  
  document.getElementById('intro_txt').innerHTML = (info['intro_txt'] == 'undefined') ? translations['H60'] : info['intro_txt'];
  document.getElementById('ang_infra_txt').innerHTML = (info['ang_infra_txt'] == 'undefined') ? translations['H60'] : info['ang_infra_txt'];
  document.getElementById('dise_facility_txt').innerHTML = (info['dise_facility_txt'] == 'undefined') ? translations['H60'] : info['dise_facility_txt'];
  //document.getElementById('lib_txt').innerHTML = (info['lib_infra_txt'] == 'undefined') ? translations['H60'] : info['lib_infra_txt'];
  //document.getElementById('neighbours_txt').innerHTML = (info['neighbours_txt'] == 'undefined') ? translations['H60'] : info['neighbours_txt'];
  document.getElementById('source_txt').innerHTML = (info['source_txt'] == 'undefined') ? translations['H60'] : info['source_txt'];
  document.getElementById('note_txt').innerHTML = (info['note_txt'] == 'undefined') ? translations['H60'] : info['note_txt'];
  document.getElementById('neighbours_txt').innerHTML = (info['neighbours_txt'] == 'undefined') ? translations['H60'] : info['neighbours_txt'];
  document.getElementById('conclusion_txt').innerHTML = (info['conclusion_txt'] == 'undefined') ? translations['H60'] : info['conclusion_txt'];
}
}

function neighbours_anginfra() {
   // Create our data table.
 if(info["neighbours_anginfra"] == undefined) {
     document.getElementById('ai_comparison').innerHTML = translations['H60'];
 } else {
   var vals = [];
   var tabletxt = ''
   var rows = Object.keys(info["neighbours_anginfra"]);
   var cols_ai = Object.keys(info["neighbours_anginfra"][rows[0]]);
   var rows_di = Object.keys(info["neighbours_dise"]);
   var cols_di = Object.keys(info["neighbours_dise"][rows_di[0]]);
   var cols = [];
   if (cols_ai.length >cols_di.length) { cols =cols_ai; }
   else { cols = cols_di; } 
   var colName = 0
   tabletxt = '<div class="div-table"><div class="div-table-row">';
   tabletxt += '<div class="div-table-col" style="width:485px"><span style="font-weight:bold;font-size:12pt">'+ translations['H82']+ '</span></div><div class="div-table-col"></div>';        
     for (var col in cols) {
        colName = parseInt(col) + 1
        if ( cols[col] == info['const_name']) 
          tabletxt += '<div class="div-table-col"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="200"><text id="vertical_black" transform="rotate(270, 12, 0) translate(-140,0)">'+cols[col]+'</text></svg></div>';        
        else
          tabletxt += '<div class="div-table-col"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="200"><text id="vertical_grey" transform="rotate(270, 12, 0) translate(-140,0)">'+cols[col]+'</text></svg></div>';        
     }
     tabletxt += '</div>';
     var prev = ''
     
     for(var i in rows){
         tabletxt += '<div class="div-table-row">';
         vals =rows[i].split('|');
         if(vals[0] == prev){
            vals[0] = '';
            tabletxt += '<div class="div-table-col" style="width:180px"></div>';
         }else{
            prev = vals[0];
            tabletxt += '<div class="div-table-col" style="width:180px">' + translations[vals[0]] + '</div>';
         }
         tabletxt += '<div class="div-table-col" style="width:300px">' + vals[1] + '</div>';
         for(var j in cols){
          if(info["neighbours_anginfra"][rows[i]][cols[j]]){
            if(parseInt(info["neighbours_anginfra"][rows[i]][cols[j]]) >= 70){
              tabletxt += '<div class="div-table-col" style="width:30px;text-align:center"><img src="/images/green_round.png" width="15px"/></div>';
            } else {
              tabletxt += '<div class="div-table-col" style="width:30px;text-align:center"><img src="/images/red_round.png" width="15px"/></div>';
            }
          } else {
              tabletxt += '<div class="div-table-col" style="width:30px;text-align:center"><img src="/images/grey_round.png" width="15px"/></div>';
          }
        }
        tabletxt += '</div>';
     }
     tabletxt += '</div>';

     /*var formatter = new google.visualization.ColorFormat();
     formatter.addRange(0, 70, '#CD4306', '#CD4306');
     formatter.addRange(70, 100, '#43AD2C', '#43AD2C');
     formatter.format(data, 2); 
     formatter.format(data, 3); 
     formatter.format(data, 4); 
     formatter.format(data, 5); 
     formatter.format(data, 6); 


     var vis = new google.visualization.Table(document.getElementById('ai_comparison'));
     vis.draw(data, {title:translations['H82'], allowHtml:true, width:500});*/
     document.getElementById('ai_comparison').innerHTML = tabletxt;
  }
}

function neighbours_dise() {
  if(info["neighbours_dise"] == undefined) {
     document.getElementById('df_comparison').innerHTML = translations['H60'];
  } else {
     var vals = [];
     var tabletxt = ''
     rows = Object.keys(info["neighbours_dise"]);
     cols = Object.keys(info["neighbours_dise"][rows[0]]);
     var colName = 0
     tabletxt = '<div class="div-table"><div class="div-table-row">';
     tabletxt += '<div class="div-table-col" style="width:485px"><span style="font-weight:bold;font-size:12pt">'+ translations['H83']+ '</span></div><div class="div-table-col"></div>';        
       for (var col in cols) {
          colName = parseInt(col) + 1 
          if ( cols[col] == info['const_name']) 
            tabletxt += '<div class="div-table-col"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="200"><text id="vertical_black" transform="rotate(270, 12, 0) translate(-140,0)">'+cols[col]+'</text></svg></div>';        
          else
            tabletxt += '<div class="div-table-col"><svg xmlns="http://www.w3.org/2000/svg" width="30" height="200"><text id="vertical_grey" transform="rotate(270, 12, 0) translate(-140,0)">'+cols[col]+'</text></svg></div>';        
       }
       tabletxt += '</div>';
       var prev = ''
       
       for(var i in rows){
           tabletxt += '<div class="div-table-row">';
           vals =rows[i].split('|');
           if(vals[0] == prev){
              vals[0] = '';
              tabletxt += '<div class="div-table-col" style="width:180px"></div>';
           }else{
              prev = vals[0];
              tabletxt += '<div class="div-table-col" style="width:180px">' + translations[vals[0]] + '</div>';
           }
           tabletxt += '<div class="div-table-col" style="width:300px">' + vals[1] + '</div>';
           for(var j in cols){
            if(info["neighbours_dise"][rows[i]][cols[j]]){
              if(parseInt(info["neighbours_dise"][rows[i]][cols[j]]) >= 70){
                tabletxt += '<div class="div-table-col" style="width:30px;text-align:center"><img src="/images/green_round.png" width="15px"/></div>';
              } else {
                tabletxt += '<div class="div-table-col" style="width:30px;text-align:center"><img src="/images/red_round.png" width="15px"/></div>';
              }
            } else {
                tabletxt += '<div class="div-table-col" style="width:30px;text-align:center"><img src="/images/grey_round.png" width="15px"/></div>';
            }
          }
          tabletxt += '</div>';
       }
       tabletxt += '</div>';
     document.getElementById('df_comparison').innerHTML = tabletxt;
  }

}


function ang_infra_table() {
      var ai_tb_str = '';
      var ai_dict = null;
      for (var key in info["ang_infra"]){
        ai_tb_str = ai_tb_str + '<span style="font-weight:bold;font-size:12pt">'+ translations[key] + '</br></span><dl class="icon-def">';
        ai_dict = info["ang_infra"][key]
        for (var each in ai_dict){ 
          disp_arr = each.split(';');
          ai_tb_str = ai_tb_str +  '<dt>' + disp_arr[0] + '</dt><dd>' + disp_arr[1] + '</br>' + ConvertToIndian(ai_dict[each],true) + '</dd>'
        }
      }
      if (ai_tb_str == '') {
        ai_tb_str = '<div style="width:200px">&nbsp;</div>'
      }
    
      document.getElementById('ang_infra_tb').innerHTML = ai_tb_str;
}


function dise_facility_table() {
      var df_tb_str = '';
      var df_dict = null;
      for (var key in info["dise_facility"]){
        df_tb_str = df_tb_str + '<span style="font-weight:bold;font-size:12pt">'+ translations[key] + '</br></span><dl class="icon-def">';
        df_dict = info["dise_facility"][key]
        for (var each in df_dict){
          disp_arr = each.split(';');
          df_tb_str = df_tb_str +  '<dt>' + disp_arr[0] + '</dt><dd>' + disp_arr[1] + '</br>' + ConvertToIndian(df_dict[each],true) + '</dd>'
        }
        df_tb_str = '</dl>' + df_tb_str + '</br>'
      }
      document.getElementById('dise_facility_tb').innerHTML = df_tb_str;
}

function lib_status_chart() {
      var data = new google.visualization.DataTable();
      data.addColumn('string' , 'Status');
      data.addColumn('string', 'Number');
      for (var key in info["lib_status"]){
        data.addRow([key , ConvertToIndian(info["lib_status"][key],false)]);
      }
      data.sort([{column:1,desc:true}]);
      var table3 = new google.visualization.Table(document.getElementById('lib_status_tb'));
      table3.draw(data, {width: 450, allowHtml: true});
}

function lib_summary_chart() {
      var data = new google.visualization.DataTable();
      data.addColumn('string' , 'Summary');
      data.addColumn('string', 'Number');
      for (var key in info["lib_summary"]){
        data.addRow([key , ConvertToIndian(info["lib_summary"][key],false)]);
      }
      data.sort([{column:1,desc:true}]);
      var table4 = new google.visualization.Table(document.getElementById('lib_summary_tb'));
      table4.draw(data, {width: 450, allowHtml: true});
}

function ConvertToIndian(inputString,colour_code) { 
      cc_str = '';
      if(colour_code){
        val = parseFloat(inputString[0]);
        bm = parseFloat(inputString[1]);
        /*if (val >= bm) {*/
        if (val >= 70) {
          cc_str = '<span style="color:#666;font-size:12pt;font-weight:bold"><span style="color:#43AD2C;">' 
        }
        else {
          cc_str = '<span style="color:#666;font-size:12pt;font-weight:bold"><span style="color:#CD4306;">' 
        }
      }
      inputString = inputString.toString(); 
      var numberArray = inputString.split('.', 2); 
      var pref = parseInt(numberArray[0]); 
      var suf = numberArray[1]; 
      var outputString = ''; 
      if (isNaN(pref)) return ''; 
      var minus = ''; 
      if (pref < 0) minus = '-'; 
      pref = Math.abs(pref).toString(); 
      if (pref.length > 3) { 
      var lastThree = pref.substr(pref.length - 3, pref.length); 
      pref = pref.substr(0, pref.length - 3); 
      if (pref.length % 2 > 0) { 
      outputString += pref.substr(0, 1) + ','; 
      pref = pref.substr(1, pref.length - 1); 
      } 

      while (pref.length >= 2) { 
      outputString += pref.substr(0, 2) + ','; 
      pref = pref.substr(2, pref.length); 
      } 

      outputString += lastThree; 
      } else { 

      outputString = minus + pref; 
      } 

      if (!isNaN(suf)) outputString += '.' + suf; 
      if(colour_code) {
        outputString = cc_str + outputString + '</span>%' 
        outputString = outputString + '<span style="font-size:8pt">&nbsp;&nbsp;&nbsp;' + translations['Bangalore Avg'] + ': ' + bm + '%</span></span>';
        return outputString; 
      } else {
        return outputString; 
      }
}

function ColourIcon(value,key) { 

      val = parseFloat(value[0]);
      /*bm = parseFloat(value[1]);
      if (val >= bm) {*/
      if (val >= 70) {
        return key;
      }
      else {
        return key.replace('.png','n.png');
      }
}
