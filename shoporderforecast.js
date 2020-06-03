
//import NeoVis from '/node_modules/neovis.js/dist/neovis.js';



function draw() {
    console.log('Drawfunction invoked')
    var config = {
        container_id: "viz",
        server_url: "bolt://localhost:7687",
        server_user: "neo4j",
        server_password: "honeywell123!",
        labels: {
            "Assembly1": {
                "caption": "name",
                "size": "pagerank",
                "community": "community"
            }
        },
        relationships: {
            "MOVES_ITEM": {
                "thickness": "weight",
                "caption": false
            }
        },
        initial_cypher: "MATCH (n)-[r:MOVES_ITEM]->(m) RETURN *"
    };

    viz = new NeoVis.default(config);
    viz.render();
}
function showSimulator(){
	alert('Simulator screen');
}

$(function () { //shorthand document.ready function
	$( "#dialog" ).dialog({ autoOpen: false });
	window.valve_type = "no";
	$('#oper_bw').hide();
	$('#vari_choice').hide();
	$('#timedurationval').hide();	
	$('#showCSV').hide();
	$(".timing").timingfield({
	  maxHour:        23,
	  width:          263,
	  hoursText:      'H',
	  minutesText:    'M',
	  secondsText:    'S',
	  hasSeconds:     true
	});
	$('.timing').hide();	
	function handleForecastData(data) { 
		console.log('Prediction received successfully!',data);
		$('#startSim').attr("disabled", false);
		$('#resetSim').attr("disabled", false);
		$(document).ajaxStop(function(){
			$.LoadingOverlay("hide");
		});
		var parseddata = JSON.parse(data);
		var date_time1 = parseddata["Completion of Entire ShopOrder"].split(" ")[1];
		console.log(date_time1);
		//var datetime = new Date(new Date().toISOString().split("T")[0]+'T' + date_time1);
		window.orig_pred_time = new Date(new Date().toISOString().split("T")[0]+'T' + date_time1);
		 $('#testResults').empty();
		 $('#clockResults').empty();
		 $('#testResults').append("Original Estimated arrival at - ",parseddata["Completion of Entire ShopOrder"]);
		 $('#testResults').append("<br/>");
		 $('#testResults').append("<div id='pendingSFCCounter'>");
		 $('#testResults').append("</div>");
		displayClockTime(date_time1);
	}
	function displayClockTime(data1) {
		svidget.load("#clockResults", { url: "clock/clock.svg", id: "clockWidget" }, { 
		data: data1, 
		backgroundColor: "#fff",
		frameColor: "#000",
		tickColor: "#000",
		hourHandColor: "#000",
		minuteHandColor: "#000",
		secondHandColor: "#f22",
		nobColor: "#777",
		tickLineType: "round",
		handLineType: "round",
		frameWidth: "10",
		labelStyle: "{}",
		animationType: "smooth",
		showLabels: "1",
		showAnimation: "0",
	});
	}
	function showSimulationResults(data) {
		console.log(data);
		//var parseddata1 = JSON.parse(data);
		$(document).ajaxStop(function(){
			$.LoadingOverlay("hide");
		});
		var sfcs_produced = $("#sfcs_no").val();
		window.shoporder_sfccount -= sfcs_produced;
		$('#pendingSFCCounter').empty();
		$('#showCSV').show();
		$('#carttime').empty();
		$('#cartdelay').empty();
		$('#clockResults').empty();
		$('#pendingSFCCounter').append("Number of pending SFC's - ",window.shoporder_sfccount);
		
		window.lastSFCtime = data["rt_forecast"];
		//window.sim_pred_time = data["shoporder_forecast"];
		$('#carttime').append(data["shoporder_forecast"]);
		var date_time1 = data["shoporder_forecast"].split(" ")[1];
		window.sim_pred_time = new Date(new Date().toISOString().split("T")[0]+'T' + date_time1);
		var diff_time_secs = Math.round(Math.abs((window.orig_pred_time - window.sim_pred_time) / 60000));
		if(diff_time_secs > 60) {
			var diff_time_hrs = Math.round(diff_time_secs / 60);
			var diff_time_mins = diff_time_secs % 60;
			//diff_time_secs = Math.round((diff_time_secs / 60) * 10 + Number.EPSILON) / 10;
			$('#cartdelay').append(diff_time_hrs+" hour "+diff_time_mins+" mins");
		}
		else {
			$('#cartdelay').append(diff_time_secs+" mins");
		}		
		console.log(date_time1);
		displayClockTime(date_time1);
		$( "#dialog" ).dialog( "close" );
	}
    $('#neo4j_form').on('submit', function (e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting
        var data = $("#neo4j_form :input").serializeArray();
        var querz = data[0]['value'];
		window.shoporder_sfccount = querz;
		var size_meter = data[1]['value'];
		var val_type = data[2]['value'];
		$(document).ajaxStart(function(){
			$.LoadingOverlay("show");
		});
        console.log(querz);
        var query_builder = {
            cypher_val: querz
        };
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:8000/monty2shoporder/" + querz + "/" +size_meter + "/" + val_type,
            success: handleForecastData,
            error: function () { console.error('Network connection to H2o Server failed!') }
        });
    });
	
    var myVar = '';
    $('#searchNode').on('click', (e) => {
        var nodeName = $('#labelnameg').val();
        var statement = `MATCH (n:${nodeName})-[r:MOVES_ITEM]->(m:${nodeName}) RETURN *`;
        viz.renderWithCypher(statement);
        console.log('Searched query is '+ nodeName);
    });
	
	$( "#dialog" ).dialog({
		  dialogClass: "no-close",
		  modal: true,
		  width: 550,
		  buttons: [
			{
			  text: "Simulate",
			  click: function() {
				var sfcscount = $("#sfcs_no").val();
				if (sfcscount.length < 1) {
					alert("Please enter the number of SFC's to simulate");
					return;
				}
				$(document).ajaxStart(function(){
					$.LoadingOverlay("show");
				});
				console.log(sfcscount);	
				var time_val = $("#timedurationval").val();
				if (time_val.length < 1) {
					time_val = "0";
				}
				else {
					time_val = Number(time_val) * 1000;
				}
				var var_type = $("#vari_choice").val();
				if(window.bw_flag == 1) {
					var oper_choice = $("#oper_choice").val();	
					$.ajax({
							type: "GET",
							url: "http://127.0.0.1:8000/gettimeseries/" + sfcscount + "/" +time_val + "?oper_choice=" + oper_choice + "&sfc_bw_choice=" + var_type + "&ventil_choice=" + window.valve_type,
							success: showSimulationResults,
							error: function () { console.error('Network connection to H2o Server failed!') }
					});					
				}	
				else {
					$.ajax({
						type: "GET",
						url: "http://127.0.0.1:8000/gettimeseries/" + sfcscount + "/" +time_val + "?ventil_choice=" + window.valve_type,
						success: showSimulationResults,
						error: function () { console.error('Network connection to H2o Server failed!') }
					});
				}		
				
			  }
			}
		  ]
		});
	$('#startSim').on('click', (e) => {
		//alert('Simulator screen');		
		$( "#dialog" ).dialog( "open" );
    });
	$('input[type=radio][name=checkbox-1]').on('change', function() {
	  switch ($(this).val()) {
		case 'Yes':
		  //alert("Simulate breakdown");
		  window.bw_flag = 1;
		  $('#oper_bw').show();
		  $('#vari_choice').show();
		  $('.timing').show();
		  $('#timedurationval').show();
		  break;
		case 'No':
		  //alert("Do not simulate breakdown");
		  window.bw_flag = 0;
		  $('#oper_bw').hide();
		  $('#vari_choice').hide();
		  $('.timing').hide();
		  $('#timedurationval').hide();
		  break;
	  }
	});
	$('input[type=radio][name=valve]').on('change', function() {
	  switch ($(this).val()) {
		case 'VE':
		  window.valve_type = "yes";
		  break;
		case 'noval':
		  window.valve_type = "no";
		  break;
	  }
	});
	$('#resetSim').on('click', (e) => {
		//alert('Simulator screen');
		window.shoporder_sfccount = 0;
		$('#testResults').empty();
		$('#clockResults').empty();
		$('#startSim').attr("disabled", true);
		$('#resetSim').attr("disabled", true);		
    });
	$('#showCSV').on('click', (e) => {
		//window.location = 'displaycsv.html';
		//window.open('http://127.0.0.1:8887/displaycsv.html');
		window.open('http://127.0.0.1:8050/');
		//window.history.pushState('obj', 'newtitle', '/displaycsv.html');
		//return false;
    });

});