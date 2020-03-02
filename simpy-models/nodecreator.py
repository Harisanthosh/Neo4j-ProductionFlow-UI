import pandas as pd
import sys

def runpg():
    file = pd.read_csv('processmining_template.csv',sep=';')
    print(file.head())
    neo4j_map = {}
    cypher_queries = {}
    neo4j_map['Name'] = []
    neo4j_map['Label'] = []
    cypher_queries['Create'] = []
    cypher_queries['Match'] = []
    """
    Actual Cypher Query
    LOAD CSV WITH HEADERS FROM 'http://localhost:8887/simpy-models/processing_template.csv' AS line
    CREATE (:Speaker { name: line.caseId})W
    """
    cypher_queries['Create'].append('http://localhost:8887/simpy-models/processing_template.csv')
    return cypher_queries


if __name__ == "__main__":
    runpg()
