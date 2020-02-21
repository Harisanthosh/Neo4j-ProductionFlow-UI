
//import NeoVis from '/node_modules/neovis.js/dist/neovis.js';


var viz;

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

    function customdraw() {
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
    }
	// setInterval(customdraw, 5000);
	customdraw();