import pandas as pd

def runpg():
    file = pd.read_csv('wc_sap.csv',sep=';')
    print(file.head())
    neo4j_map = {}
    neo4j_map['Name'] = []
    neo4j_map['Label'] = []
    wc_leader_arr = []
    # Use .values.tolist() to convert the Pandas Series to python list
    label_extr = file['Label'].values.tolist()
    neo4j_map['Name'].append(file['ResourceName'].values.tolist())
    neo4j_map['Label'].append(label_extr)
    # print(neo4j_map)
    cypher_creater = ""

    for key,val in enumerate(label_extr):
        if len(val) < 6:
            wc_leader_arr.append(1)
        else:
            wc_leader_arr.append(0)

    file['Leader'] = wc_leader_arr
    neo4j_map['Leader'] = wc_leader_arr
    print(file.head())

    for key,val in enumerate(label_extr):
        if key == 0:
            cypher_creater += f'CREATE (:Gaszähler {{name: {val}, processname: {neo4j_map["Name"][key][key]}}}),'
        elif (key == len(label_extr)-1):
            cypher_creater += f' (:Gaszähler {{name: {val}, processname: {neo4j_map["Name"][0][key]}}}))'
        else:
            cypher_creater += f' (:Gaszähler {{name: {val}, processname: {neo4j_map["Name"][0][key]}}})),'

    print(cypher_creater)

if __name__ == "__main__":
    runpg()
