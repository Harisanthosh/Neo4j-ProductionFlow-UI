import pandas as pd

def runpg():
    file = pd.read_csv('wc_sap.csv',sep=';')
    print(file.head())
    neo4j_map = {}
    neo4j_map['Name'] = []
    neo4j_map['Label'] = []
    # Use .values.tolist() to convert the Pandas Series to python list
    label_extr = file['Label'].values.tolist()
    neo4j_map['Name'].append(file['ResourceName'].values.tolist())
    neo4j_map['Label'].append(label_extr)
    # print(neo4j_map)
    cypher_creater = ""
    for key,val in enumerate(label_extr):
        # print(key,val)
        if key == 0:
            cypher_creater += f'CREATE (:{val} {{name: {neo4j_map["Name"][key][key]}}}),'
        elif key == len(label_extr)-1:
            cypher_creater += f' (:{val})'
        else:
            cypher_creater += f' (:{val}),'
    print(cypher_creater)

if __name__ == "__main__":
    runpg()
