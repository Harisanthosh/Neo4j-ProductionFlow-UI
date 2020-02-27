
//import NeoVis from '/node_modules/neovis.js/dist/neovis.js';


var viz;

var config = {
    container_id: "viz",
    server_url: "bolt://localhost:7687",
    server_user: "neo4j",
    server_password: "honeywell123!",
    labels: {
        "Gaszähler": {
            "caption": "name"
        }
    },
    relationships: {
        "GEHÖRT_ZU": {
            "thickness": "weight",
            "caption": false
        }
    },
    initial_cypher: "MATCH (n)-[r:GEHÖRT_ZU]->(m) RETURN *"
};

viz = new NeoVis.default(config);
viz.render();

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

function customrenderer(querz) {
    var labelname = querz.split(':')[1].split('{')[0].trim();
    console.log(labelname);
    var config = {
        container_id: "viz",
        server_url: "bolt://localhost:7687",
        server_user: "neo4j",
        server_password: "honeywell123!",
        labels: {
            labelname: {
                "caption": "name"
            }
        },
        relationships: {
            "LINKED_WITH": {
                "thickness": "weight",
                "caption": false
            }
        },
        initial_cypher: "MATCH (n)-[r:LINKED_WITH]->(m) RETURN *"
    };

    viz = new NeoVis.default(config);
    viz.render();
}

$(function () { //shorthand document.ready function
    $('#neo4j_form').on('submit', function (e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting
        var data = $("#neo4j_form :input").serializeArray();
        var querz = data[0]['value'];
        console.log(querz);
        var query_builder = {
            cypher_val: querz
        };
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/createnodes/" + querz,
            data: JSON.stringify(query_builder),
            success: function () { console.log('Created Node successfully'); customrenderer(querz); },
            error: function () { console.error('Network connection to Neo4j failed!') }
        });
    });
    var myVar = '';
    $('#startSim').on('click', (e) => {
        myVar = setInterval(function () {
            // viz = NeoVis.reload();
            viz.reload();
        }, 3000);
    });

    $('#stopSim').on('click', (e) => {
        clearInterval(myVar);
    });
});