
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
	$( "#dialog2" ).dialog({ autoOpen: false });
	$( "#dialog3" ).dialog({ autoOpen: false });
	$( "#dialog-message" ).dialog({ autoOpen: false });	
	$( "#configSettingsSim" ).dialog({ autoOpen: false });
	window.valve_type = "no";
	window.line_item = 2;
	$('#oper_bw').hide();
	$('#vari_choice').hide();
	$('#timedurationval').hide();	
	$('#showCSV').hide();
	$('#configForecast').hide();
	$('#outputTable').hide();
	$(".timing").timingfield({
	  maxHour:        23,
	  width:          263,
	  hoursText:      'H',
	  minutesText:    'M',
	  secondsText:    'S',
	  hasSeconds:     true
	});
	$('#datetimepicker').datetimepicker();
	$('#datetimepicker1').datetimepicker();
	$('#datetimepicker2').datetimepicker();
	$('#datetimepicker3').datetimepicker();
	$('.timing').hide();	
	
	var tempSelect = JSON.parse(localStorage.getItem('meterConfig')) || [];
	var $select = $('#meter_prod_id'); 
	$select.find('option').remove();  
	$.each(tempSelect,function(key, value) 
	{
		$select.append('<option value=' + key + '>' + value['item_no'] + '</option>');
	});
	function GetDates(startDate, daysToAdd) {
		var aryDates = [];

		for (var i = 0; i <= daysToAdd; i++) {
			var currentDate = new Date();
			currentDate.setDate(startDate.getDate() + i);
			aryDates.push(DayAsString(currentDate.getDay()) + ", " + currentDate.getDate() + " " + MonthAsString(currentDate.getMonth()) + " " + currentDate.getFullYear());
		}

		return aryDates;
	}
	function enableDatePicker(selid) {
		$(selid).datetimepicker();
	}

	function MonthAsString(monthIndex) {
		var d = new Date();
		var month = new Array();
		month[0] = "January";
		month[1] = "February";
		month[2] = "March";
		month[3] = "April";
		month[4] = "May";
		month[5] = "June";
		month[6] = "July";
		month[7] = "August";
		month[8] = "September";
		month[9] = "October";
		month[10] = "November";
		month[11] = "December";

		return month[monthIndex];
	}

	function DayAsString(dayIndex) {
		var weekdays = new Array(7);
		weekdays[0] = "Sunday";
		weekdays[1] = "Monday";
		weekdays[2] = "Tuesday";
		weekdays[3] = "Wednesday";
		weekdays[4] = "Thursday";
		weekdays[5] = "Friday";
		weekdays[6] = "Saturday";

		return weekdays[dayIndex];
	}

	var startDate = new Date();
	var aryDates = GetDates(startDate, 7);
	window.dateMapper = aryDates;
	window.timeShifts = {
		"Early":"05:45 – 13:30",
		"Late":"14:00 – 21:45",
		"Night":"22:15 – 05:15"
	}
	//console.log(aryDates);​
	for(var xt=0; xt < aryDates.length-1; xt++) {
		//console.log(cx[xt]);
		var day_str = aryDates[xt].split(",")[0];
		var date_str = aryDates[xt].split(",")[1];
		$("#dayHeader"+xt).empty();
		$("#dateHeader"+xt).empty();
		$("#dayHeader"+xt).append(day_str);
		$("#dateHeader"+xt).append(date_str);
	}
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
	function handleNewForecastData(data) { 
		console.log('Prediction received successfully!',data);
		$(document).ajaxStop(function(){
			$.LoadingOverlay("hide");
		});
		var parseddata = JSON.parse(data);
		var date_time1 = parseddata["Completion of Entire ShopOrder"].split(" ")[1];
		console.log(date_time1);
		//var datetime = new Date(new Date().toISOString().split("T")[0]+'T' + date_time1);
		$('#estimatedDate1').empty();
		$('#estimatedDate1').append(parseddata["Completion of Entire ShopOrder"]);
	}
	function handleDynamicForecastData(data) { 
		console.log('Prediction received successfully!',data);
		$(document).ajaxStop(function(){
			$.LoadingOverlay("hide");
		});
		var parseddata = JSON.parse(data);
		var date_time1 = parseddata["Completion of Entire ShopOrder"].split(" ")[1];
		console.log(date_time1);
		var selectedRow = window.current_selrow ;
		var itemid = selectedRow.split('m')[1];
		//var sfc_count = $(this).closest("tr").find("#sfcrowItem"+itemid).text().trim();
		$('#estimatedDate'+itemid).empty();
		$('#estimatedDate'+itemid).append(parseddata["Completion of Entire ShopOrder"]);
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
		var act_diff_secs = window.orig_pred_time - window.sim_pred_time;
		var diff_time_secs = Math.round(Math.abs(act_diff_secs / 60000));
		//if prediction is lesser than the actual arrival time, no delay
		if(act_diff_secs >0) {
			$('#carttime').empty();
			$('#carttime').append(window.orig_pred_time.toLocaleString());
			$('#cartdelay').append("No ");
		}
		else if(diff_time_secs > 60) {
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
	$('#formMeter').on('submit', function (e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting
        var data = $("#formMeter :input").serializeArray();
        var querz = data[0]['value'];
		window.shoporder_sfccount = querz;
		var size_meter = data[1]['value'];
		var val_type = data[2]['value'];
		var atex_type = data[3]['value'];
		$(document).ajaxStart(function(){
			$.LoadingOverlay("show");
		});
        console.log(querz);
        var query_builder = {
            item_no: querz,
			meter_size: size_meter,
			val_config: val_type,
			atex_config: atex_type
        };
		var oldConfig = JSON.parse(localStorage.getItem('meterConfig')) || [];
		oldConfig.push(query_builder);
		localStorage.setItem('meterConfig', JSON.stringify(oldConfig));
		$( "#dialog-message" ).dialog( "open" );
		$( "#dialog-message" ).dialog({
		  modal: true,
		  buttons: {
			Ok: function() {
			  $( this ).dialog( "close" );
			}
		  }
		});
		$(document).ajaxStop(function(){
			$.LoadingOverlay("hide");
		});
    });
	$('#shiftForm').on('submit', function (e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting
        var data = $("#shiftForm :input").serializeArray();
        //var querz = data[0]['value'];
		//window.pred_key = querz;
		$(document).ajaxStart(function(){
			$.LoadingOverlay("show");
		});
        //console.log(querz);
		$('#durationShifts').empty();
		var shiftz = [];
		var selIDs = [];
		var dates_shifts = {};   
		var obj_arr = [];
		$('.activetd').each(function(){ 
			//console.log($(this).innerHTML);
			var curr_shift_name = $(this)[0].innerText;
			var curr_shift = $(this)[0].id;
			shiftz.push(curr_shift_name);
			selIDs.push(curr_shift);
			var date_idx = Number(curr_shift.split("Shift")[1]);
			dates_shifts["day"] = window.dateMapper[date_idx];
			dates_shifts["shift"] = curr_shift_name;
			obj_arr.push(dates_shifts);
			dates_shifts = {};   
			
		});
		console.log(shiftz);
		console.log(selIDs);
		console.log(obj_arr);
		window.time_shifts = obj_arr;
		var totalshifts = shiftz.length;
		console.log(totalshifts);
		$('#durationShifts').append("<h3>Production Runtime for this week - "+totalshifts*8+"</h3>");
		$('#configForecast').show();
		$('#outputTable').show();
		$(document).ajaxStop(function(){
			$.LoadingOverlay("hide");
		});
    });
	$('#lineItem1').on('submit', function (e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting
		//window.shoporder_sfccount = querz;
		$(document).ajaxStart(function(){
			$.LoadingOverlay("show");
		});
        var query_builder = {
            cypher_val: 800
        };
		var oldConfig = JSON.parse(localStorage.getItem('meterConfig')) || [];
		var item_prep = oldConfig[window.pred_key];
		var querz = 800;
		var size_meter = item_prep['meter_size'];
		var val_type = item_prep['val_config'];
		console.log(item_prep);
		$('#startDate1').empty();
		$('#startDate1').append(new Date().toLocaleString());
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:8000/monty2shoporder/" + querz + "/" +size_meter + "/" + val_type,
            success: handleNewForecastData,
            error: function () { console.error('Network connection to H2o Server failed!') }
        });
    });
	/*$('#closeItem1').on('submit', function (e) { 
        e.preventDefault();  
		$(document).ajaxStart(function(){
			$.LoadingOverlay("show");
		});
		alert("Remove Order");
		$(document).ajaxStop(function(){
					$.LoadingOverlay("hide");
		});
    });*/
	$("#outputTable").on("click", "form" , function(e) {
            //$(this).parent().remove();
			e.preventDefault();  //prevent form from submitting
			var selectedRow = $(this)[0].id;
			window.current_selrow = selectedRow;
			if(selectedRow.includes("close")) {
				//alert("Remove Order");
				var remove_id = Number(selectedRow.split("Item")[1]);
				//$("#rowItem"+remove_id).remove();
				$( "#dialog3" ).dialog( "open" );
				$("#predDate").empty();
				$("#accuScore").empty();
				var pred_time = $(this).closest("tr").find("#estimatedDate"+remove_id).text().trim();
				$("#predDate").append(pred_time);
			}
			else {
				var itemid = selectedRow.split('m')[1];
				var sfc_count = $(this).closest("tr").find("#sfcrowItem"+itemid).text().trim();
				var start_time = $(this).closest("tr").find("#timeItem"+itemid).text().trim();
				
				//var parsed_time = moment(new Date(start_time)).format("YYYY-MM-DD HH:mm:ss");
				var parsed_time = moment(start_time, "DD/MM/YYYY HH:mm:ss").format("YYYY-MM-DD HH:mm:ss");
				$(document).ajaxStart(function(){
					$.LoadingOverlay("show");
				});
				var query_builder = {
					cypher_val: 800
				};
				var oldConfig = JSON.parse(localStorage.getItem('meterConfig')) || [];
				var item_prep = oldConfig[window.pred_key];
				var querz = sfc_count;
				var size_meter = item_prep['meter_size'];
				var val_type = item_prep['val_config'];
				console.log(item_prep);
				//$('#startDate1').empty();
				//$('#startDate1').append(new Date().toLocaleString());
				var url_sim1 = "http://127.0.0.1:8000/monty2shoporder/" + querz + "/" +size_meter + "/" + val_type + "?datetime1=" + parsed_time;
				/*$.ajax({
					type: "GET",
					url: "http://127.0.0.1:8000/monty2shoporder/" + querz + "/" +size_meter + "/" + val_type + "?query_shifts=" + window.time_shifts,
					success: handleDynamicForecastData,
					error: function () { console.error('Network connection to H2o Server failed!') }
				});*/
				$.ajax({
						contentType: 'application/json',
						data: JSON.stringify({"shifts":window.time_shifts}),
						dataType: 'json',
						success: handleDynamicForecastData,
						error: function(){
							console.log("Device control failed");
						},
						processData: false,
						type: 'POST',
						url: url_sim1
					});	
			}
				
      });
	  $("#outputTable").on("click", "a" , function(e) {
		  var selectedRow = $(this)[0].id;
		  window.current_selrow = selectedRow;
		  if(selectedRow.includes("delete")) {
				//alert("Remove Order");
				var remove_id = Number(selectedRow.split("Item")[1]);
				$("#rowItem"+remove_id).remove();
			}
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
				var nc_count = $("#nccases").val();
				if (nc_count.length < 1) {
					nc_count = "0";
				}
				var var_type = $("#vari_choice").val();
				if(window.bw_flag == 1) {
					var oper_choice = $("#oper_choice").val();	
					$.ajax({
							type: "GET",
							url: "http://127.0.0.1:8000/gettimeseries/" + sfcscount + "/" +time_val + "?oper_choice=" + oper_choice + "&sfc_bw_choice=" + var_type + "&ventil_choice=" + window.valve_type + "&nc_cases=" + nc_count,
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
	$( "#dialog2" ).dialog({
		  dialogClass: "no-close",
		  modal: true,
		  width: 550,
		  buttons: [
			{
			  text: "Add",
			  click: function() {
				var sfcscount = $("#sfcs_no_qty").val();
				if (sfcscount.length < 1) {
					alert("Please enter the number of SFC's to simulate");
					return;
				}
				$(document).ajaxStart(function(){
					$.LoadingOverlay("show");
				});
				window.line_item += 1;
				//var item_type = $("#meter_prod_id").val();
				var item_type = $("#meter_prod_id option:selected").text();
				var start_date_order = $("#datetimepickerval").val();
				console.log(item_type);
				console.log(start_date_order);	
				var parsed_time = moment(new Date(start_date_order)).format("DD/MM/YYYY HH:mm:ss");
				var markup = "<tr id=rowItem"+ window.line_item +"><td id=sfcrowItem"+ window.line_item +">" + sfcscount + "</td><td>" + item_type + "</td><td id=timeItem"+ window.line_item +">" + parsed_time + "</td><td id=estimatedDate"+ window.line_item +">" + "" + "</td><td><form name='closeItem1' id=closeItem"+ window.line_item +"><input type='submit' class='submit center-block btn btn-primary' value='Close'></form> <a id=deleteItem"+ window.line_item +" href='' target='_blank' style='margin-left: 7vw;' onclick='return false;'>Delete</a> </td> <td><form name='lineItem1' id=lineItem"+ window.line_item +"><input type='submit' class='submit center-block btn btn-primary' value='Forecast'></form> </td> </tr>";
				//var markup = "<tr id=rowItem"+ window.line_item +"><td id=sfcrowItem"+ window.line_item +">" + sfcscount + "</td><td>" + item_type + "</td><td id=timeItem"+ window.line_item +">" + parsed_time + "</td><td id=estimatedDate"+ window.line_item +">" + "" + "</td><td><div class='input-group date' id='datetimepicker"+ window.line_item +"'><input type='text' class='form-control' /><span class='input-group-addon'><span class='glyphicon glyphicon-calendar'></span></span></div></td><td><form name='lineItem1' id=lineItem"+ window.line_item +"><input type='submit' class='submit center-block btn btn-primary' value='Forecast'></form> </td> </tr>";
				enableDatePicker('#datetimepicker'+ window.line_item);
				$("#outputTable").append(markup);
				$(document).ajaxStop(function(){
					$.LoadingOverlay("hide");
				});
				$( "#dialog2" ).dialog("close" );				
			  }
			}
		  ]
		});
	$( "#dialog3" ).dialog({
		  dialogClass: "no-close",
		  modal: true,
		  width: 630,
		  buttons: [
			{
			  text: "Close",
			  click: function() {
				var sfcscount = $("#datetimepickerval3").val();
				if (sfcscount.length < 1) {
					alert("Please enter the date for Closing order");
					return;
				}
				$(document).ajaxStart(function(){
					$.LoadingOverlay("show");
				});
				$(document).ajaxStop(function(){
					$.LoadingOverlay("hide");
				});
				$( "#dialog3" ).dialog("close" );
				//var parsed_time = moment(new Date(start_date_order)).format("DD/MM/YYYY HH:mm:ss");
				//var markup = "<tr id=rowItem"+ window.line_item +"><td id=sfcrowItem"+ window.line_item +">" + sfcscount + "</td><td>" + item_type + "</td><td id=timeItem"+ window.line_item +">" + parsed_time + "</td><td id=estimatedDate"+ window.line_item +">" + "" + "</td><td><form name='closeItem1' id=closeItem"+ window.line_item +"><input type='submit' class='submit center-block btn btn-primary' value='Close'></form></td> <td><form name='lineItem1' id=lineItem"+ window.line_item +"><input type='submit' class='submit center-block btn btn-primary' value='Forecast'></form> </td> </tr>";
						
			  }
			}
		  ]
		});
		
	$( "#configSettingsSim" ).dialog({
		  dialogClass: "no-close",
		  modal: true,
		  width: 550,
		  buttons: [
			{
			  text: "Create",
			  click: function() {
				$(document).ajaxStart(function(){
					$.LoadingOverlay("show");
				});
				if(window.wt_flag == 1) {
					var url_sim = 'http://127.0.0.1:8000/createwaitingtimesimulator';
					var dict_config = {
					  "name": "simulator monty2",
					  "ventiltype": window.valve_type,
					  "stutzen_befetten_waiting_time": $("#stutzen").val() || 27,
					  "aussenmagnet_montieren_waiting_time": $("#montieren").val() || 47,
					  "messwerk_einsetzen_waiting_time": $("#einsetzen").val() || 24,
					  "oberteil_dosieren_waiting_time": $("#Oberteil").val() || 11,
					  "unterteil_aufsetzen_waiting_time": $("#aufsetzen").val() || 4,
					  "falz_auflegen_waiting_time": $("#auflegen").val() || 11,
					  "zähler_vorbördeln_waiting_time": $("#vorbördeln").val() || 8,
					  "zähler_fertigbördeln_waiting_time": $("#fertigbördeln").val() || 4,
					  "zähler_dichtheitsprüfen_waiting_time": $("#dichtheitsprüfen").val() || 42,
					  "zähler_abstapeln_waiting_time": $("#abstapeln").val() || 70,
					  "version": 1
					};
				}
				else {
					var url_sim = 'http://127.0.0.1:8000/createsimulator';
					var dict_config = {
					  "name": "simulator monty2",
					  "ventiltype": window.valve_type,
					  "stutzen_befetten_time": $("#stutzen").val() || 5,
					  "aussenmagnet_montieren_time": $("#montieren").val() || 6,
					  "messwerk_einsetzen_time": $("#einsetzen").val() || 9,
					  "oberteil_dosieren_time": $("#Oberteil").val() || 12,
					  "unterteil_aufsetzen_time": $("#aufsetzen").val() || 18,
					  "falz_auflegen_time": $("#auflegen").val() || 8,
					  "zähler_vorbördeln_time": $("#vorbördeln").val() || 10,
					  "zähler_fertigbördeln_time": $("#fertigbördeln").val() || 11,
					  "zähler_dichtheitsprüfen_time": $("#dichtheitsprüfen").val() || 35,
					  "zähler_abstapeln_time": $("#abstapeln").val() || 21,
					  "version": 1
					};
				}
				
				$.ajax({
					contentType: 'application/json',
					data: JSON.stringify(dict_config),
					dataType: 'json',
					success: function(data){
						console.log(data);
						$(document).ajaxStop(function(){
							$.LoadingOverlay("hide");
						});
						$( "#configSettingsSim" ).dialog("close" );
					},
					error: function(){
						console.log("Device control failed");
					},
					processData: false,
					type: 'POST',
					url: url_sim
				});				
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
	$('#meter_prod_id').on('change', function() {
		window.pred_key = $(this).val();
	});
	$('#configSim').on('click', (e) => {
		//alert('Simulator screen');		
		$( "#configSettingsSim" ).dialog( "open" );
    });
	$('#resetSim').on('click', (e) => {
		//alert('Simulator screen');
		window.shoporder_sfccount = 0;
		$('#testResults').empty();
		$('#clockResults').empty();
		$('#startSim').attr("disabled", true);
		$('#resetSim').attr("disabled", true);	
		$('#showCSV').hide();
    });
	$('#showCSV').on('click', (e) => {
		//window.location = 'displaycsv.html';
		//window.open('http://127.0.0.1:8887/displaycsv.html');
		window.open('http://127.0.0.1:8050/');
		//window.history.pushState('obj', 'newtitle', '/displaycsv.html');
		//return false;
    });
	$('.meterconfig').on('click', (e) => {
		window.open('http://127.0.0.1:8887/meterconfig.html');
    });
	$('.mining').on('click', (e) => {
		window.open('http://127.0.0.1:8887/forecastdashboard.html');
    });
	$('#configForecast').on('click', (e) => {
		var tempVal = JSON.parse(localStorage.getItem('meterConfig')) || [];
		var $select = $('#meter_prod_id1'); 
		$select.find('option').remove();  		
		$.each(tempVal,function(key, value) 
		{
			$select.append('<option value=' + key + '>' + value['item_no'] + '</option>');
		});
		$( "#dialog2" ).dialog( "open" );
		//window.open('http://127.0.0.1:8887/shoporder.html');
    });
	$("#shiftTable td").click(function() {
		if($(this).hasClass("activetd")) {
			$(this).removeClass("activetd");
		}
		else {
			$(this).addClass("activetd");
		}
	});
	$("#datetimepicker3").on('dp.change', function() {
		//console.log($(this).val());		
		$('#accuScore').empty();
		//var parsed_time = moment(new Date($(this).val())).format("DD/MM/YYYY HH:mm:ss");
		moment($("#predDate").text(), "DD/MM/YYYY HH:mm:ss")
		var pred_date = moment($("#predDate").text(), "DD/MM/YYYY HH:mm:ss");
		var parsed_time = moment(new Date($("#datetimepickerval3").val()));
		var diff_hours = parsed_time.diff(pred_date, 'hours');
		var acc_calc = Math.round((parsed_time.diff(pred_date) / parsed_time * 100000 + Number.EPSILON) * 100) / 100;
		$('#accuScore').append(acc_calc + ' %');
		//$('#accuScore').append(Math.random()*100);
	});
	/*$("#datetimepickerval3").change(function(){
	   console.log($(this).val());	
	  //alert("The text has been changed.");
	});*/
	$('input[type=radio][name=checkbox-5]').on('change', function() {
	  switch ($(this).val()) {
		case 'Yes':
		  window.wt_flag = 1;
		  //$('#oper_bw').show();
		  $("label[for='stutzen']").text("Enter Waiting time for Stutzen befetten (in secs)");
		  $("label[for='montieren']").text("Enter Waiting time for Aussenmagnet montieren (in secs)");
		  $("label[for='einsetzen']").text("Enter Waiting time for Messwerk einsetzen (in secs)");
		  $("label[for='dosieren']").text("Enter Waiting time for Oberteil dosieren (in secs)");
		  $("label[for='aufsetzen']").text("Enter Waiting time for Unterteil aufsetzen (in secs)");
		  $("label[for='auflegen']").text("Enter Waiting time for Falz auflegen (in secs)");
		  $("label[for='vorbördeln']").text("Enter Waiting time for Zähler vorbördeln (in secs)");
		  $("label[for='fertigbördeln']").text("Enter Waiting time for Zähler fertigbördeln (in secs)");
		  $("label[for='dichtheitsprüfen']").text("Enter Waiting time for Zähler dichtheitsprüfen (in secs)");
		  $("label[for='abstapeln']").text("Enter Waiting time for Zähler abstapeln (in secs)");		  
		  break;
		case 'No':
		  window.wt_flag = 0;
		  //$('#oper_bw').hide();
		  $("label[for='stutzen']").text("Enter time for Stutzen befetten (in secs)");
		  $("label[for='montieren']").text("Enter time for Aussenmagnet montieren (in secs)");
		  $("label[for='einsetzen']").text("Enter time for Messwerk einsetzen (in secs)");
		  $("label[for='dosieren']").text("Enter time for Oberteil dosieren (in secs)");
		  $("label[for='aufsetzen']").text("Enter time for Unterteil aufsetzen (in secs)");
		  $("label[for='auflegen']").text("Enter time for Falz auflegen (in secs)");
		  $("label[for='vorbördeln']").text("Enter time for Zähler vorbördeln (in secs)");
		  $("label[for='fertigbördeln']").text("Enter time for Zähler fertigbördeln (in secs)");
		  $("label[for='dichtheitsprüfen']").text("Enter time for Zähler dichtheitsprüfen (in secs)");
		  $("label[for='abstapeln']").text("Enter time for Zähler abstapeln (in secs)");
		  break;
	  }
	});

});