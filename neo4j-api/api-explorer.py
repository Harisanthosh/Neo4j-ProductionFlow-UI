from fastapi import FastAPI, File, Form, UploadFile
from starlette.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Set
import sys
import json
from neo4j import GraphDatabase
import nxneo4j
import subprocess
import string
from datetime import datetime

from pydantic import BaseModel
import h2o
h2o.init()
#sys.path.insert(1, 'C:/Users/H395978/PycharmProjects/Neo4j-ProductionFlow-UI/simpy-models')
#import h2oexplorer
import MEFI3RegressionTrees as mefi3
sys.path.insert(1, 'C:/Users/H395978/PycharmProjects/Neo4j-ProductionFlow-UI/simpy-models/')
import Monty2Simulator as mty2
import simulateddata_viewer as simview
#import PMFormatter as pm

origins = [
    "http://127.0.0.1",
    "http://localhost:8887",
    "http://127.0.0.1:8887/"
]


class ConfigSimulator(BaseModel):
    name: str
    ventiltype: str = None
    stutzen_befetten_time: float
    aussenmagnet_montieren_time: float
    messwerk_einsetzen_time: float
    oberteil_dosieren_time: float
    unterteil_aufsetzen_time: float
    falz_auflegen_time: float
    zähler_vorbördeln_time: float
    zähler_fertigbördeln_time: float
    zähler_dichtheitsprüfen_time: float
    zähler_abstapeln_time: float
    version: float

class ConfigSimulatorWaitingTime(BaseModel):
    name: str
    ventiltype: str = None
    stutzen_befetten_waiting_time: float
    aussenmagnet_montieren_waiting_time: float
    messwerk_einsetzen_waiting_time: float
    oberteil_dosieren_waiting_time: float
    unterteil_aufsetzen_waiting_time: float
    falz_auflegen_waiting_time: float
    zähler_vorbördeln_waiting_time: float
    zähler_fertigbördeln_waiting_time: float
    zähler_dichtheitsprüfen_waiting_time: float
    zähler_abstapeln_waiting_time: float
    version: float

class DateShift(BaseModel):
    day: str
    shift: str


class Shifts(BaseModel):
    shifts: List[DateShift] = None

app = FastAPI(title="Gas Meter API", description="API testing interface by Honeywell's Production Intelligence team")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    #pm.invoker_api(start_time,end_time)
    return {"Simulator Started!"}

@app.get("/preparedata")
def prepare_production_log():
    #pm.invoker_api(start_time,end_time)
    subprocess.call([r'C:\Users\H395978\PycharmProjects\Neo4j-ProductionFlow-UI\workflow_automater.bat'])
    return {"Executing KNIME Workflow"}

@app.post("/createnodes/{graph_query}")
def create_graph(graph_query: str):
    cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    return cx.create_graph(graph_query)
    #return {"item_id": item_id, "q": q}

@app.get("/gettimeseries/{sfc_quantity}/{variation}")
def get_timeduraration_of_shoporder(sfc_quantity: str, variation: str,oper_choice: str = None,sfc_bw_choice: str = None,ventil_choice: str = None,nc_cases: str = None,orig_sfc_qty: str = None):
    ventil_flag = ventil_choice if ventil_choice != None else "no"
    last_date = mty2.api_invoker(ventil_flag,sfc_quantity,variation,oper_choice,sfc_bw_choice,nc_cases)
    #Add condtion to control last date for normal simulation run
    if oper_choice == None:
        last_date = None
    rt_forecast = mefi3.sim_pred_formulator()
    #shop_forecast_val = mefi3.monty_shift_so_forecaster(rt_forecast,sfc_quantity,last_date)
    shop_forecast_val = mefi3.monty_shift_so_forecaster_updated(rt_forecast,sfc_quantity,orig_sfc_qty,last_date)
    #sfc_query = int(sfc_quantity) / 150
    #shop_forecast_val = mefi3.timeseries_shoporder_monty_millis(rt_forecast,int(sfc_quantity),sfc_query,None)
    #shop_forecast_val = mefi3.ts_shoporder_monty_forecaster(rt_forecast,sfc_quantity)
    return {"rt_forecast":rt_forecast, "shoporder_forecast":shop_forecast_val}

@app.post("/createsimulator/")
async def config_simulator(item: ConfigSimulator):
    item_dict = item.dict()
    mty2.create_simulator(item_dict)
    return item_dict

@app.post("/createwaitingtimesimulator/")
async def config_waiting_time_simulator(item: ConfigSimulatorWaitingTime):
    item_dict = item.dict()
    mty2.create_waiting_time_simulator(item_dict)
    return item_dict

@app.get("/shoporder/{sfc_quantity}")
def get_shoporder_forecast_mefi3(sfc_quantity: str):
    #cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    estimate = mefi3.estimate_shoporder(sfc_quantity)
    forecast = mefi3.arima_predictor()
    return {f"Forecast for the shop order is on {estimate} as {int(forecast[0])} SFC's can be produced in the next hour!"}

@app.get("/montyshoporder/{sfc_quantity}/{casing}/{ventil}")
def get_monty_shoporder_forecast(sfc_quantity: str,casing: str, ventil: str):
    #cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
    #estimate = h2oexplorer.estimate_shoporder(sfc_quantity)
    estimate, time_ms  = mefi3.estimate_shoporder_monty(sfc_quantity, casing, ventil)
    forecast = mefi3.monty_arima_predictor()
    return {f"Forecast for the shop order is on {estimate} as {int(forecast[0])} SFC's can be produced in the next hour!"}

@app.get("/monty2/{sfc_quantity}/{casing}/{ventil}")
def monty2_shoporder_forecaster(sfc_quantity: str,casing: str, ventil: str):
    estimate, time_ms = mefi3.estimate_shoporder_monty(sfc_quantity, casing, ventil)
    print(f"the time in ms is {time_ms} and the time taken for one SFC completion is {estimate}")
    forecast = mefi3.monty_arima_predictor()
    final_time = mefi3.estimate_timeseries_shoporder_monty(time_ms,int(sfc_quantity))
    time = {}
    time['Single SFC'] = estimate
    time['Entire ShopOrder'] = final_time
    return json.dumps(time)

@app.get("/monty2shoporder/{sfc_quantity}/{casing}/{ventil}")
def monty2_total_shoporder_forecast(sfc_quantity: str,casing: str, ventil: str, datetime: str = None,query_shifts: str = None):
    """
    Datetime field is optional, if not provided it will estimate from the current time of execution
    [Note]: Enter datetime in the following format YYYY-MM-DD HH:MM:SS example:2020-04-27 19:35:00
    """
    #estimate, time_ms = mefi3.estimate_shoporder_monty(sfc_quantity, casing, ventil)
    estimate, time_ms = mefi3.estimate_sfc_totaltime(sfc_quantity, casing, ventil,datetime)
    #estimate_sfc_totaltime
    print(f"the time in ms is {time_ms} and the time taken for one SFC completion is {estimate}")
    if query_shifts != None:
        print(query_shifts)
    sfc_query = int(sfc_quantity) / 150
    final_time = mefi3.timeseries_shoporder_monty_millis(time_ms,int(sfc_quantity),sfc_query,datetime)
    time = {}
    time['Arrival of First SFC'] = estimate
    time['Completion of Entire ShopOrder'] = final_time
    return json.dumps(time)

@app.post("/monty2shoporder/{sfc_quantity}/{casing}/{ventil}")
def monty2_total_shoporder_forecast_with_shifts(shift:Shifts, sfc_quantity: str,casing: str, ventil: str, datetime1: str = None):
    """
    Datetime field is optional, if not provided it will estimate from the current time of execution
    [Note]: Enter datetime in the following format YYYY-MM-DD HH:MM:SS example:2020-04-27 19:35:00
    """
    #estimate, time_ms = mefi3.estimate_sfc_totaltime(sfc_quantity, casing, ventil,datetime)
    #estimate_sfc_totaltime 1032.65
    #print(f"the time in ms is {time_ms} and the time taken for one SFC completion is {estimate}")
    item_dict = shift.dict()
    #print(item_dict)
    sfc_query = int(sfc_quantity) / 150
    orig_date = datetime.strptime(datetime1,'%Y-%m-%d %H:%M:%S')
    final_time = mefi3.timeseries_shoporder_monty_millis(1032.65,int(sfc_quantity),sfc_query,datetime1)
    my_date = datetime.strptime(final_time,'%d-%m-%Y %H:%M:%S')
    parsed_date = my_date.strftime('%d/%m/%Y %H:%M:%S %p')
    print(parsed_date)
    curr_shift = mty2.shift_estimator(orig_date,my_date,item_dict)
    #print(f"The predicted time is in {curr_shift} Shift!")
    time = {}
    #time['Arrival of First SFC'] = estimate
    time['Completion of Entire ShopOrder'] = curr_shift
    return json.dumps(time)


# @app.get("/getcentrality")
# def get_closeness_centrality_of_graph():
#     cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
#     return cx.get_closeness_centrality()
#
# @app.get("/betweennesscentrality")
# def get_betweeness_centrality_of_graph():
#     cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
#     return cx.get_betweenness_centrality()
#
# @app.get("/harmoniccentrality")
# def get_harmonic_centrality_of_graph():
#     cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
#     return cx.get_harmonic_centrality()
#
# @app.get("/shortestpath")
# def get_shortest_path_between_two_nodes(p1: str,p2: str):
#     cx = GraphAlgorithms("bolt://localhost:7687", "neo4j", "honeywell123!")
#     return cx.get_shortest_path(p1,p2)
