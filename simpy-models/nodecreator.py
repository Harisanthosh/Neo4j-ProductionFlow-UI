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
    
    LOAD CSV WITH HEADERS FROM "http://localhost:8887/simpy-models/processmining_template.csv" AS line FIELDTERMINATOR ';' 
    MATCH(s:Speaker{name:line.caseId}),(s1:Stage) CALL apoc.create.relationship(s, line.Activity,{time:line.Timestamp}, s1) YIELD rel
    REMOVE rel.noOp
    """
    cypher_queries['Create'].append("CREATE CONSTRAINT ON (n:Speaker) ASSERT n.name IS UNIQUE\n LOAD CSV WITH HEADERS FROM 'http://localhost:8887/simpy-models/processmining_template.csv' AS line FIELDTERMINATOR ';' MERGE (s:Speaker{name:line.caseId}) RETURN count(s)")
    cypher_queries['Match'].append("LOAD CSV WITH HEADERS FROM 'http://localhost:8887/simpy-models/processmining_template.csv' AS line FIELDTERMINATOR ';' MATCH(s:Speaker{name:line.caseId}),(s1:Stage) CALL apoc.create.relationship(s, line.Activity,{time:line.Timestamp}, s1) YIELD rel REMOVE rel.noOp")
    print(cypher_queries)
    return cypher_queries


if __name__ == "__main__":
    runpg()
