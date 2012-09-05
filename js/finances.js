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
  translations = info['transdict']
  now = new Date()
  document.getElementById("reportdate").innerHTML = now.toDateString();
  document.getElementById("rephead").innerHTML = "<img src=\'/images/KLP_logo2.png\' width='130px' vertical-align='top' border=0 />" + '<br/>' + translations['H56'];
  document.getElementById("summaryhead").innerHTML = translations['H66'];
  document.getElementById("tlmhead").innerHTML = translations['H67'];
  /*document.getElementById("annualhead").innerHTML = 'Allocation based on Category';//translations['H29'];
  document.getElementById("mntnchead").innerHTML = 'Allocation for Maintenance'; //translations['H36'];*/
  document.getElementById("neighhead").innerHTML = translations['H68'];

  document.getElementById("constname").innerHTML = translations[info["const_type"]] + " <img src=\'../images/arrow.gif\' width='8px' vertical-align='center' border='0'/>" + "<br/><h1>"  
                                                 + info['const_name'] + "</h1>";
  document.getElementById("constinfo").innerHTML =  "<dl class='header-def'><dt>" + translations['H8'] + "</dt><dd>" + info["const_code"] + "</dd>"
                                                + "<dt>" + translations['H9'] + "</dt><dd>" + info["const_rep"] + "</dd>"
                                                + "<dt>" + translations['H10'] + "</dt><dd>" + info["const_party"] + "</dd></dl>";
  document.getElementById("hiddenip").innerHTML = '<input type="hidden" name="const_type" value="'+ info["constype"] + '" />' +
          '<input type="hidden" name="const_id" value="'+ info["const_id"] + '" />' +
          '<input type="hidden" name="forreport" value="'+ info["forreport"] + '" />' +
          '<input type="hidden" name="rep_lang" value="'+ info["rep_lang"] + '" />' ;
  document.getElementById('instcounts').innerHTML = '<dl class=\'header-def\'><dt style="font-size:9pt">' + translations['H11'] + '</dt><dd style="font-size:9pt">' + info["inst_counts"]["abs_schcount"] + '<dt style="font-size:9pt">' + translations['H72'] + '</dt><dd style="font-size:9pt">' + info["inst_counts"]["fin_schcount"] +'</dd></dl>';
  if(parseInt(info["inst_counts"]["abs_schcount"]) != 0){
    neighbours_Chart();
    annual_Chart();
    mntnc_Chart();
    total_Chart();
    document.getElementById('intro_txt').innerHTML = (info['intro_txt'] == 'undefined') ? translations['H60'] : info['intro_txt'];
    document.getElementById('summary_txt').innerHTML = (info['summary_txt'] == 'undefined') ? translations['H60'] : info['summary_txt'];
    document.getElementById('tlm_txt').innerHTML = (info['tlm_txt'] == 'undefined') ? translations['H60'] : info['tlm_txt'];
    document.getElementById('annual_txt').innerHTML = (info['annual_txt'] == 'undefined') ? translations['H60'] : info['annual_txt'];
    document.getElementById('mtnc_txt').innerHTML = (info['mtnc_txt'] == 'undefined') ? translations['H60'] : info['mtnc_txt'];
    document.getElementById('neighbours_txt').innerHTML = (info['neighbours_txt'] == 'undefined') ? translations['H60'] : info['neighbours_txt'];
    document.getElementById('source_txt').innerHTML = (info['source_txt'] == 'undefined') ? translations['H60'] : info['source_txt'];
  }
}

function neighbours_Chart() {

      // Create our data table.
      var data = new google.visualization.DataTable();
      var chartdata = new google.visualization.DataTable();
      var colors = [];
      var max = 0
      data.addColumn('string', translations['H6']);
      data.addColumn('string', 'TLM');
      data.addColumn('string', 'SG');
      data.addColumn('string', 'SMG');
      data.addColumn('string', 'Total');
      chartdata.addColumn('string', translations['H6']);
      chartdata.addColumn('number', 'Total');
      chartdata.addColumn('string', 'Label');
      if (isEmpty(info["neighbours_grant"]) == false ) {
        for (var key in info["neighbours_grant"]){
            tlm = parseInt(info["neighbours_grant"][key]['tlm'])
            annual = parseInt(info["neighbours_grant"][key]['annual'])
            mntnc = parseInt(info["neighbours_grant"][key]['mntnc'])
            data.addRow([key, ConvertToIndian(tlm),ConvertToIndian(annual),ConvertToIndian(mntnc), ConvertToIndian(tlm+annual+mntnc)]);
            count = tlm + annual + mntnc
            chartdata.addRow([key.replace('BANGALORE','B. '), count,ConvertToIndian(count)]);
            if (count > max) max = count;
            if (key == info['const_name']){
              colors.push('31A354')
            } else {
              colors.push('BAE4B3')
            }
        }
        colors = colors.join('|');

        var vis = new google.visualization.ImageChart(document.getElementById('neighboursdata'));
        var options = {
            chbh: 'r,1.5,0.5',
            chs: '350x160',
            cht: 'bhs',
            chco: colors,
            chxt: 'y',
            chxr: '1,0,'+ Math.round(max),
            chm:'N*cINR*,000000,0,-1,11,0',
            chxs:'3,000000,12,0,t',
            chts: '000000,12,l',
            chds:'0,'+max,
            legend: 'none'
          };
        vis.draw(chartdata, options);

        var table1 = new google.visualization.Table(document.getElementById('neighboursdata_tb'));
        table1.draw(data, {width: 510, allowHtml: true, showRowNumber: false});

        /*var chart1 = new google.visualization.PieChart(document.getElementById('neighboursdata'));
      chart1.draw(chartdata, {width: 400, height: 200, title: translations['H62'],colors:['006D2C','31A354','74C476','BAE4B3','DCE7D8']});*/
    }
}

function annual_Chart() {
      var data = new google.visualization.DataTable();
      data.addColumn('string' , translations['H45']);
      data.addColumn('number', 'Amount');
      data.addColumn('number', translations['H53']+translations['H54']);
      data.addColumn('string', translations['H69']);
      for (var key in info["annualgrant_sch"]){
        key_str = '';
        data.addRow([translations[key] + ' ' + translations['H52'], parseInt(info["annualgrant_sch"][key][1]), parseInt(info["annualgrant_sch"][key][0]), ConvertToIndian(info["annualgrant_sch"][key][1])]);
      }
      var tabview2 = new google.visualization.DataView(data);
      tabview2.setColumns([0,2,3]); 
      var chartview2 = new google.visualization.DataView(data);
      chartview2.setColumns([0,1]);
      data.sort([{column:1,desc:true}]);
      var table2 = new google.visualization.Table(document.getElementById('annualgrantsch_tb'));
      table2.draw(tabview2, {width: 450, allowHtml: true});
      var chart2 = new google.visualization.PieChart(document.getElementById('annualgrantsch'));
      chart2.draw(chartview2, {width: 450, height: 200, title: translations['H63'],colors:['006D2C','31A354','74C476','BAE4B3','EDF8E9']});
}

function mntnc_Chart() {
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H70']);
      data.addColumn('number', 'Amount');
      data.addColumn('number', translations['H53']+translations['H54']);
      data.addColumn('string', translations['H69']);
      for (var key in info["mtncgrant_sch"]){
          data.addRow([translations[key], parseInt(info["mtncgrant_sch"][key][1]),parseInt(info["mtncgrant_sch"][key][0]),ConvertToIndian(info["mtncgrant_sch"][key][1])]);
      }
      var tabview3 = new google.visualization.DataView(data);
      tabview3.setColumns([0,2,3]); 
      var chartview3 = new google.visualization.DataView(data);
      chartview3.setColumns([0,1]);
      var table3 = new google.visualization.Table(document.getElementById('mntncgrantsch_tb'));
      table3.draw(tabview3, {width: 450,allowHtml: true});
      var chart3 = new google.visualization.PieChart(document.getElementById('mntncgrantsch'));
      chart3.draw(chartview3, {width: 450, height: 200, title: translations['H64'],colors: ['006D2C','31A354','74C476','BAE4B3','EDF8E9']});
}

function total_Chart() {
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H71']);
      data.addColumn('number', 'Amount');
      data.addColumn('string', translations['H69']);
      data.addRow(['TLM', info["total_tlm"],ConvertToIndian(String(info["total_tlm"]))]);
      data.addRow(['SG', info["total_annual"],ConvertToIndian(String(info["total_annual"]))]);
      data.addRow(['SMG', info["total_mntc"],ConvertToIndian(String(info["total_mntc"]))]);

      var tabview = new google.visualization.DataView(data);
      tabview.setColumns([0,2]);
      var table4 = new google.visualization.Table(document.getElementById('totalsch_tb'));
      table4.draw(tabview,{width: 400 ,  allowHtml: true, showRowNumber: false});

      var chartview = new google.visualization.DataView(data);
      chartview.setColumns([0,1]);
      var chart4 = new google.visualization.PieChart(document.getElementById('totalsch'));
      chart4.draw(chartview, {width: 450, height: 200, title: translations['H65'],colors: ['006D2C','31A354','74C476','BAE4B3','EDF8E9']});
}

function ConvertToIndian(inputString) { 
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
      return '<img src="/images/Rupee.jpg"/>&nbsp;' + outputString; 
}
