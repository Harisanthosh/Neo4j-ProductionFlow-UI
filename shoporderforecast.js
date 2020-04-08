
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

$(function () { //shorthand document.ready function
	function handleForecastData(data) { 
		console.log('Prediction received successfully!',data);
		 $('#myLogFile').append(data);
	}
    $('#neo4j_form').on('submit', function (e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting
        var data = $("#neo4j_form :input").serializeArray();
        var querz = data[0]['value'];
        console.log(querz);
        var query_builder = {
            cypher_val: querz
        };
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:8000/shoporder/" + querz,
            success: handleForecastData,
            error: function () { console.error('Network connection to Neo4j failed!') }
        });
    });
	
    var myVar = '';
    $('#searchNode').on('click', (e) => {
        var nodeName = $('#labelnameg').val();
        var statement = `MATCH (n:${nodeName})-[r:MOVES_ITEM]->(m:${nodeName}) RETURN *`;
        viz.renderWithCypher(statement);
        console.log('Searched query is '+ nodeName);
    });

});