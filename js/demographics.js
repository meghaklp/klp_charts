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

      
function initialise(data)
{

  info = data;
  translations = info['transdict']
  now = new Date()
  document.getElementById("reportdate").innerHTML = now.toDateString();
  document.getElementById("rephead").innerHTML = "<img src=\'../images/KLP_logo2.png\' width='130px' vertical-align='top' border=0 />" + '<br/>' + translations['H56'];
//  document.getElementById("rephead").innerHTML =  translations['H56'];
  document.getElementById("schoolhead").innerHTML = translations['H13'];
  document.getElementById("gendhead").innerHTML = translations['H24'];
  document.getElementById("enrolhead").innerHTML = translations['H29'];
  document.getElementById("langhead").innerHTML = translations['H36'];
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
  document.getElementById('instcounts').innerHTML = '<dl class=\'header-def\'><dt>' + translations['H11'] + '</dt><dd>' + info["inst_counts"]["schcount"] + '</dd>'
                                                  + '<dt>' + translations['H12'] + '</dt><dd>' + info["inst_counts"]["preschcount"] + '</dd></dl>';
  if(parseInt(info["inst_counts"]["schcount"]) != 0){
    gend_sch_Chart();
    mt_sch_Chart();
    moi_sch_Chart();
    cat_sch_Chart();
    enrol_sch_Chart();
  }
  if(parseInt(info["inst_counts"]["preschcount"]) != 0){
    mt_presch_Chart();
    gend_presch_Chart();
    enrol_presch_Chart();
  }
  if(info["neighbours_sch_hasdata"] != 0) {
    neighbours_sch_Chart();
    //neighbours_sch_table();
    neighbours_gendsch_Chart();
  }
  if(info["neighbours_presch_hasdata"] != 0) {
    neighbours_presch_Chart();
    //neighbours_presch_table();
    neighbours_gendpresch_Chart();
  }
  if (info["forreport"] == undefined){
    document.getElementById('sch_txt').innerHTML = (info['sch_txt'] == 'undefined') ? translations['H60'] : info['sch_txt'];
    document.getElementById('presch_txt').innerHTML = (info['presch_txt'] == 'undefined') ? translations['H60'] : info['presch_txt'];
    document.getElementById('lang_txt').innerHTML = (info['lang_txt'] == 'undefined') ? translations['H60'] : info['lang_txt'];
    document.getElementById('neighbours_txt').innerHTML = (info['neighbours_txt'] == 'undefined') ? translations['H60'] : info['neighbours_txt'];
    document.getElementById('enrol_txt').innerHTML = (info['enrol_txt'] == 'undefined') ? translations['H60'] : info['enrol_txt'];
    document.getElementById('source_txt').innerHTML = translations['H61'];// Source
  } else {
    document.report_form.sch_txt.value = info['sch_txt'];//Category + Enrolment Schools
    document.report_form.presch_txt.value = info['presch_txt']; // Gender
    document.report_form.enrol_txt.value = info['enrol_txt']; //Preschool
    document.report_form.lang_txt.value = info['lang_txt']; // Moi & MT schools
    document.report_form.neighbours_txt.value = info['neighbours_txt']; // Neighbours
    document.report_form.source_txt.value = translations['H61'];// Source
  }
}

function neighbours_sch_Chart() {

      // Create our data table.
      var data = new google.visualization.DataTable();
      var colors = [];
      var max = 0
      data.addColumn('string', translations['H6']);
      data.addColumn('number', translations['H11']);
      for (var key in info["neighbours_sch"]){
          count = parseInt(info["neighbours_sch"][key]['schcount'])
          data.addRow([key, count]);
          if (count > max) max = count;
          if (key == info['const_name']){
            colors.push('31A354')
          } else {
            colors.push('BAE4B3')
          }
      }
      /*var chartn8 = new google.visualization.BarChart(document.getElementById('neighbourssch'));
      chartn8.draw(data, {width: 500, height: 200, title: translations['H41'],colors:['006D2C','31A354','74C476','BAE4B3','EDF8E9'],legend:'none'});*/
      colors = colors.join('|');
      
      var vis = new google.visualization.ImageChart(document.getElementById('neighbourssch'));
      var options = {
          chbh: 'r,1.5,0.5',
          chs: '450x200',
          cht: 'bhs',
          chco: colors,
          chxt: 'y',
          chxr: '1,0,'+ Math.round(max),
          chm:'N ** schools,000000,0,-1,11',
          //chdl:'Comparison',
          chxs:'3,000000,12,0,t',
          chts: '000000,12,l',
          chds:'0,'+max,
          legend: 'none'
        };
      vis.draw(data, options);
      /*    chtt: translations['H41'],
          chts: '000000,12,l',*/ 
      document.getElementById('neighbourssch_head').innerHTML = translations['H41']
}

function neighbours_gendsch_Chart() {
  if(info["neighbours_gendsch_hasdata"] != 0) {
      // Create our data table.
      var colors1 = []
      var colors2 = []
      var max = 0
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H6']);
      data.addColumn('number', translations['H27']);
      data.addColumn('number', translations['H28']);
      for (var key in info["neighbours_sch"]){
          data.addRow([key, parseInt(info["neighbours_sch"][key]['Boy']),parseInt(info["neighbours_sch"][key]['Girl'])]);
          count = parseInt(info["neighbours_sch"][key]['Boy'])
          if (count > max) max = count;
          count = parseInt(info["neighbours_sch"][key]['Girl'])
          if (count > max) max = count;

          if (key == info['const_name']){
            colors1.push('E35804')
            colors2.push('31A354')
          } else {
            colors1.push('F3B590')
            colors2.push('BAE4B3')
          }
      }
      colors1 = colors1.join('|');
      colors2 = colors2.join('|');
      var vis = new google.visualization.ImageChart(document.getElementById('neighboursgendsch'));
      var options = {
          chbh: 'r,0.5,1.5',
          chxt: 'y',
          chs: '450x200',
          cht: 'bhg',
          chco: colors1 + ',' + colors2,
          chts: '000000,12,l',
          chm:'N ** boys,000000,0,-1,11|N ** girls,000000,1,-1,11',
          chxs:'3,000000,12,0,t',
          chds:'0,'+max+',0,'+max,
          legend: 'none'
      }
      vis.draw(data, options);
  }
}

function neighbours_sch_table() {
  if(info["neighbours_sch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H6']);
      //data.addColumn('number', translations['H11']);
      data.addColumn('number', translations['H57']); 
      //data.addColumn('number', translations['H28']);
      for (var key in info["neighbours_sch"]){
          var gend_ratio = -roundNumber((1-parseInt(info["neighbours_sch"][key]['Girl'])/parseInt(info["neighbours_sch"][key]['Boy'])),2);
          var ratio_str =''
          if (parseInt(info["neighbours_sch"][key]['Girl'])>parseInt(info["neighbours_sch"][key]['Boy'])){
            ratio_str = '    '+translations['H59']+':'+ info["neighbours_sch"][key]['Girl']+' > ' + translations['H58']+':' + info["neighbours_sch"][key]['Boy'] 
          } else {
            ratio_str = '    ' + translations['H58']+':'+ info["neighbours_sch"][key]['Boy']+' > ' + translations['H59']+':' + info["neighbours_sch"][key]['Girl'] 
          }
          //data.addRow([key, parseInt(info["neighbours_sch"][key]['schcount']),{v:gend_ratio,f:gend_ratio.toString()+'%'}]);
          data.addRow([key,{v:gend_ratio,f:gend_ratio.toString()+ratio_str}]);
      }
      data.sort([{column:0}]);
      var table7 = new google.visualization.Table(document.getElementById('neighbourssch_tb'));
      var formatter = new google.visualization.ArrowFormat();
      formatter.format(data, 1); // Apply formatter to second column
      table7.draw(data, {width: 400, allowHtml: true, showRowNumber: false});
  }
}

function neighbours_presch_Chart() {
  if(info["neighbours_presch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      var max = 0;
      var colors = [];
      data.addColumn('string', translations['H6']);
      data.addColumn('number', translations['H12']);
      for (var key in info["neighbours_presch"]){
          count = parseInt(info["neighbours_presch"][key]['preschcount'])
          data.addRow([key,count]);
          if (count > max) max = count;
          if (key == info['const_name']){
            colors.push('31A354')
          } else {
            colors.push('BAE4B3')
          }
      }
      /*var chartn9 = new google.visualization.BarChart(document.getElementById('neighbourspresch'));
      chartn9.draw(data, {width: 500, height: 200, title: translations['H42'],colors:['006D2C','31A354','74C476','BAE4B3','EDF8E9'],legend:'none'});*/
      colors = colors.join('|');
      var vis = new google.visualization.ImageChart(document.getElementById('neighbourspresch'));
      var options = {
          chbh: 'r,1.5,0.5',
          chs: '450x200',
          cht: 'bhs',
          chco: colors,
          chxt: 'y',
          chxr: '1,0,'+ Math.round(max),
          chm:'N ** preschools,000000,0,-1,11',
          //chdl:'Comparison',
          chxs:'3,000000,12,0,t',
          chts: '000000,12,l',
          chds:'0,'+max,
          legend: 'none'
        };
      vis.draw(data, options);
      document.getElementById('neighbourspresch_head').innerHTML = translations['H42']
  }
}

function neighbours_gendpresch_Chart() {
  if(info["neighbours_gendpresch_hasdata"] != 0) {
      // Create our data table.
      var colors1 = [];
      var colors2 = [];
      var max = 0
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H6']);
      data.addColumn('number', translations['H27']);
      data.addColumn('number', translations['H28']);
      for (var key in info["neighbours_presch"]){
          data.addRow([key, parseInt(info["neighbours_presch"][key]['Boy']),parseInt(info["neighbours_presch"][key]['Girl'])]);
          count = parseInt(info["neighbours_presch"][key]['Boy'])
          if (count > max) max = count;
          count = parseInt(info["neighbours_presch"][key]['Girl'])
          if (count > max) max = count;
          if (key == info['const_name']){
            colors1.push('E35804')
            colors2.push('31A354')
          } else {
            colors1.push('F3B590')
            colors2.push('BAE4B3')
          }
      }
      colors1 = colors1.join('|');
      colors2 = colors2.join('|');
      var vis = new google.visualization.ImageChart(document.getElementById('neighboursgendpresch'));
      var options = {
          chbh: 'r,0.5,1.5',
          chxt: 'y',
          chs: '450x200',
          cht: 'bhg',
          chco: colors1 + ',' + colors2,
          chts: '000000,12,l',
          chm:'N ** boys,000000,0,-1,11|N ** girls,000000,1,-1,11',
          chxs:'3,000000,12,0,t',
          chds:'0,'+max+',0,'+max,
          legend: 'none'
        };
      vis.draw(data, options);
  }
}

function neighbours_presch_table() {
  if(info["neighbours_presch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H6']);
      data.addColumn('number', translations['H57']);
      for (var key in info["neighbours_presch"]){
        var gend_ratio = -roundNumber((1-parseInt(info["neighbours_presch"][key]['Girl'])/parseInt(info["neighbours_presch"][key]['Boy'])),2);
        var ratio_str =''
        if (parseInt(info["neighbours_presch"][key]['Girl'])>parseInt(info["neighbours_presch"][key]['Boy'])){
            ratio_str = '    '+translations['H59']+':'+ info["neighbours_presch"][key]['Girl']+' > ' + translations['H58']+':' + info["neighbours_presch"][key]['Boy']
        } else {
            ratio_str = '    ' + translations['H58']+':'+ info["neighbours_presch"][key]['Boy']+' > ' + translations['H59']+':' + info["neighbours_presch"][key]['Girl']
          }
        //data.addRow([key, parseInt(info["neighbours_presch"][key]['preschcount']),{v:gend_ratio,f:gend_ratio.toString()+'%'}]);
        data.addRow([key, {v:gend_ratio,f:gend_ratio.toString()+ratio_str}]);
      }
      data.sort([{column:0}]);
      var table8 = new google.visualization.Table(document.getElementById('neighbourspresch_tb'));
      var formatter = new google.visualization.ArrowFormat();
      formatter.format(data, 1); // Apply formatter to second column
      table8.draw(data, {width: 400, allowHtml: true, showRowNumber: false});
  }
}

function enrol_sch_Chart() {
  if(info["enrol_sch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string' , translations['H45']);
      data.addColumn('number', translations['H46']);
      for (var key in info["enrol_sch_tb"]){
        key_str = '';
        data.addRow([translations[key] + ' ' + translations['H52'], parseInt(info["enrol_sch_tb"][key])]);
      }
      data.sort([{column:1,desc:true}]);
      var table9 = new google.visualization.Table(document.getElementById('enrolsch_tb'));
      table9.draw(data, {width: 400});
      var chart8 = new google.visualization.BarChart(document.getElementById('enrolsch'));
      chart8.draw(data, {width: 400, height: 240, title: translations['H30'],colors:['006D2C','31A354','74C476','BAE4B3','EDF8E9'],legend:'none'});
  }
}

function enrol_presch_Chart() {
  if(info["enrol_presch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H47']);
      data.addColumn('number', translations['H46']);
      for (var key in info["enrol_presch_tb"]){
          data.addRow([translations[key], parseInt(info["enrol_presch_tb"][key])]);
      }
      data.sort([{column:1}]);
      var table10 = new google.visualization.Table(document.getElementById('enrolpresch_tb'));
      table10.draw(data, {width: 400});
      var chart9 = new google.visualization.BarChart(document.getElementById('enrolpresch'));
      chart9.draw(data, {width: 400, height: 100, title: translations['H31'],colors:['006D2C','31A354','74C476','BAE4B3','EDF8E9'],legend:'none'});
  }
}

function moi_sch_Chart() {
  if(info["moi_sch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H48']);
      data.addColumn('number', translations['H11']);
      for (var key in info["moi_sch_tb"]){
          data.addRow([translations[key] + translations['H50'], parseInt(info["moi_sch_tb"][key])]);
      }
      data.sort([{column:1,desc:true}]);
      var table11 = new google.visualization.Table(document.getElementById('moisch_tb'));
      table11.draw(data, {width: 400});
      var chart3 = new google.visualization.PieChart(document.getElementById('moisch'));
      chart3.draw(data, {width: 400, height: 240, title: translations['H14'],colors: ['006D2C','31A354','74C476','BAE4B3','EDF8E9']});
  }
}

function cat_sch_Chart() {
  if(info["cat_sch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H45']);
      data.addColumn('number', translations['H11']);
      for (var key in info["cat_sch_tb"]){
          data.addRow([ translations[key] + translations['H52'], parseInt(info["cat_sch_tb"][key])]);
      }
      data.sort([{column:1,desc:true}]);
      var table4 = new google.visualization.Table(document.getElementById('catsch_tb'));
      table4.draw(data,{width: 400});
      var chart3 = new google.visualization.PieChart(document.getElementById('catsch'));
      chart3.draw(data, {width: 400, height: 240, title: translations['H15'],colors: ['006D2C','31A354','74C476','BAE4B3','EDF8E9']});
  }
}

function gend_sch_Chart() {
  if(info["gend_sch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H24']);
      data.addColumn('number', translations['H49']);
      data.addRows([
        [translations['H27'], info["gend_sch_tb"]["Boy"]],
        [translations['H28'], info["gend_sch_tb"]["Girl"]],
      ]);
      var table2 = new google.visualization.Table(document.getElementById('gendsch_tb'));
      table2.draw(data,{width:350, height: 120});
      var chart1 = new BarsOfStuff(document.getElementById('gendsch'));
      chart1.draw(data, {width:350, height: 240, title:translations['H26']});
  }
}

function gend_presch_Chart() {
  if(info["gend_presch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H24']);
      data.addColumn('number', translations['H49']);
      data.addRows([
        [translations['H27'], info["gend_presch_tb"]["Boy"]],
        [translations['H28'], info["gend_presch_tb"]["Girl"]],
      ]);
      var table3 = new google.visualization.Table(document.getElementById('gendpresch_tb'));
      table3.draw(data,{width:350, height: 120});
      var chart2 = new BarsOfStuff(document.getElementById('gendpresch'));
      chart2.draw(data, {width:350, height: 240, title:translations['H25']});
  }
}

function mt_presch_Chart() {
  if(info["mt_presch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H39']);
      data.addColumn('number', ' ');
      for (var key in info["mt_presch_tb"]){
          data.addRow([translations[key], parseInt(info["mt_presch_tb"][key])]);
      }
      data.sort([{column:1,desc:true}]);
      var table4 = new google.visualization.Table(document.getElementById('mtpresch_tb'));
      table4.draw(data,{width: 400});
      var chart3 = new google.visualization.PieChart(document.getElementById('mtpresch'));
      chart3.draw(data, {width: 400, height: 200, title: translations['H38'],colors: ['006D2C','31A354','74C476','BAE4B3','EDF8E9']});
  }
}

function mt_sch_Chart() {
  if(info["mt_sch_hasdata"] != 0) {
      // Create our data table.
      var data = new google.visualization.DataTable();
      data.addColumn('string', translations['H39']);
      data.addColumn('number', ' '); //translations['H49']);
      for (var key in info["mt_sch_tb"]){
          data.addRow([translations[key], parseInt(info["mt_sch_tb"][key])]);
      }
      data.sort([{column:1,desc:true}]);
      var table5 = new google.visualization.Table(document.getElementById('mtsch_tb'));
      table5.draw(data,{width: 400});
      var chart4 = new google.visualization.PieChart(document.getElementById('mtsch'));
      chart4.draw(data, {width: 400, height: 240, title:  translations['H37'], colors: ['006D2C','31A354','74C476','BAE4B3','EDF8E9']});
  }
}
