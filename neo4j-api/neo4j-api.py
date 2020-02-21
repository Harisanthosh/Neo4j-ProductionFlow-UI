import sys
import datetime
from neo4j import GraphDatabase
import nxneo4j
from flask import Flask
from flask import request
from flask import json
from flask_cors import CORS
import querymaker as qr

# Initialize as Flask APP
app = Flask(__name__,static_url_path='')
CORS(app)
class GraphAlgorithms(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message,name,weightclass):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message,name,weightclass)
            print(greeting)

    def create_graph(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_manager, message)
            print(greeting)
            return greeting

    def get_greetings(self):
        with self._driver.session() as session:
            gnodes = session.write_transaction(self._get_greetings)
            nodesArr = []
            # nodesArr['Label'] = []
            # nodesArr['Properties'] = []
            for item in gnodes:
                print(f'{item}')
                nodesArr.append(item[0])
                # nodesArr['Label'].append(item["n.name"])
                # nodesArr['Properties'].append(item["n.machineid"])
            # print(gnodes)
            return json.dumps(nodesArr)

    # def get_closeness_centrality(self):
    #     with self._driver.session() as session:
    #         gnodes = session.write_transaction(self._get_centrality)
    #         lst = []
    #         for item in gnodes:
    #             print(f'{item}')
    #             lst.append(item)
    #         print(gnodes)
    #         return lst

    def get_closeness_centrality(self):
        with self._driver.session() as session:
            G = nxneo4j.Graph(self._driver, config)
            sorted_cc = sorted(nxneo4j.centrality.closeness_centrality(G, wf_improved=False).items(),
                               key=lambda x: x[1], reverse=True)
            for name, score in sorted_cc[:10]:
                print(name, score)
            return sorted_cc

    def get_page_rank(self):
        with self._driver.session() as session:
            G = nxneo4j.Graph(self._driver, config)
            sorted_pagerank = sorted(nxneo4j.centrality.pagerank(G).items(), key=lambda x: x[1], reverse=True)
            for name, score in sorted_pagerank[:10]:
                print(name, score)
            return sorted_pagerank

    def get_betweenness_centrality(self):
        with self._driver.session() as session:
            G = nxneo4j.Graph(self._driver, config)
            sorted_bw = sorted(nxneo4j.centrality.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)
            for name, score in sorted_bw[:10]:
                print(name, score)
            return sorted_bw

    def get_harmonic_centrality(self):
        with self._driver.session() as session:
            G = nxneo4j.Graph(self._driver, config)
            sorted_hc = sorted(nxneo4j.centrality.harmonic_centrality(G).items(), key=lambda x: x[1], reverse=True)
            for name, score in sorted_hc[:10]:
                print(name, score)
            return sorted_hc

    def get_shortest_path(self, p1, p2):
        with self._driver.session() as session:
            G = nxneo4j.Graph(self._driver, config)
            return nxneo4j.path_finding.shortest_path(G, p1, p2)

    @staticmethod
    def _create_and_return_greeting(tx, message,name,weightclass):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "SET a.name = $name "
                        "SET a.weightclass = $weightclass "
                        "RETURN a.message + ', from node ' + id(a)", message=message,name=name,weightclass=weightclass)
        return result.single()[0]

    @staticmethod
    def _create_manager(tx, message):
        result = tx.run(message)
        return result
        #return result.single()[0]

    @staticmethod
    def _get_greetings(tx):
        rxx = tx.run("MATCH (n:Assembly1)"
                     "RETURN COLLECT({resource:n.name, id:n.machineid, score:n.pagerank}) AS jsonOutput LIMIT 25")
        return rxx

    # @staticmethod
    # def _get_centrality(tx):
    #     rxx = tx.run("CALL algo.closeness.stream('Node', 'LINK')"
    #                  "YIELD nodeId, centrality"
    #                  ""
    #                  "RETURN algo.asNode(nodeId).id AS node, centrality"
    #                  "ORDER BY centrality DESC"
    #                  "LIMIT 20;")
    #     return rxx

    @staticmethod
    def _get_centrality(tx):
        rxx = tx.run("CALL algo.closeness.stream('Node', 'LINK')"
                     "YIELD nodeId, centrality")
        return rxx


@app.route("/")
def read_root():
    return {"Hello": "World"}

@app.route("/readwc")
def read_workcenter():
    dict_return = qr.runpg()
    return json.dumps(dict_return)

@app.route("/createnodes/{graph_query}")
def create_graph(graph_query: str):
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.create_graph(graph_query)
    #return {"item_id": item_id, "q": q}

@app.route("/getnodes")
def get_nodes_from_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_greetings()


@app.route("/getcentrality")
def get_closeness_centrality_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_closeness_centrality()

@app.route("/getrank")
def get_rank_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_page_rank()

@app.route("/betweennesscentrality")
def get_betweeness_centrality_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_betweenness_centrality()

@app.route("/harmoniccentrality")
def get_harmonic_centrality_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_harmonic_centrality()
