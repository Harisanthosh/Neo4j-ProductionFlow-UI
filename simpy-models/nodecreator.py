import pandas as pd
import sys

def runpg():
    file = pd.read_csv('processmining_template.csv',sep=';')
    print(file.head())
    print(file.columns)
    neo4j_map = {}
    cypher_queries = {}
    neo4j_map['Name'] = []
    neo4j_map['Label'] = []
    cypher_queries['Create'] = []
    cypher_queries['Match'] = []
    """
    Actual Cypher Query
    file:///C:/Users/H395978/PycharmProjects/Neo4j-ProductionFlow-UI/simpy-models/processing_template.csv
    LOAD CSV WITH HEADERS FROM 'http://localhost:8887/simpy-models/processmining_template.csv' AS line FIELDTERMINATOR ';'
    CREATE (:Speaker { name: line.caseId})
    """
    cypher_queries['Create'].append("LOAD CSV WITH HEADERS FROM 'http://localhost:8887/simpy-models/processmining_template.csv' AS line FIELDTERMINATOR ';' CREATE (:Speaker { name: line.caseId})")
    print(cypher_queries)
    return cypher_queries


if __name__ == "__main__":
    runpg()
