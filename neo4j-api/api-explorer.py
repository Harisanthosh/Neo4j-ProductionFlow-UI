from fastapi import FastAPI, File, Form, UploadFile
from starlette.middleware.cors import CORSMiddleware
import pandas as pd
import sys
import json
from neo4j import GraphDatabase
import nxneo4j
sys.path.insert(1, 'C:/Users/H395978/PycharmProjects/Neo4j-ProductionFlow-UI/simpy-models')
import PMFormatter as pm

origins = [
    "http://localhost",
    "http://localhost:8887",
]
app = FastAPI(title="Graph Algorithms", description="Create and execute graph algorithms in neo4j")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = {
    "node_label": "Paper",
    "relationship_type": None,
    "identifier_property": "name"
}


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
            nodesArr = []
            for item in greeting:
                nodesArr.append(item[0])
            return json.dumps(nodesArr)

    def get_greetings(self):
        with self._driver.session() as session:
            gnodes = session.write_transaction(self._get_greetings)
            for item in gnodes:
                print(f'{item}')
            print(gnodes)
            return gnodes

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

@app.post("/files/")
async def upload_result(
    fileb: UploadFile = File(...)
):
    return {
        # "file_size": len(fileb.file.read()),
        "fileb_content_type": fileb.content_type,
    }

# @app.delete("/files/{table}")
# def remove_table(table: str):
#     return {"Hello": table}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/startsimulator/{start_time}/{end_time}")
def start_simulator(start_time: str, end_time: str):
    pm.invoker_api(start_time,end_time)
    return {"Simulator Started!"}

@app.post("/createnodes/{graph_query}")
def create_graph(graph_query: str):
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.create_graph(graph_query)
    #return {"item_id": item_id, "q": q}

@app.get("/getnodes")
def get_nodes_from_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_greetings()


@app.get("/getcentrality")
def get_closeness_centrality_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_closeness_centrality()

@app.get("/getrank")
def get_rank_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_page_rank()

@app.get("/betweennesscentrality")
def get_betweeness_centrality_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_betweenness_centrality()

@app.get("/harmoniccentrality")
def get_harmonic_centrality_of_graph():
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_harmonic_centrality()

@app.get("/shortestpath")
def get_shortest_path_between_two_nodes(p1: str,p2: str):
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.get_shortest_path(p1,p2)
