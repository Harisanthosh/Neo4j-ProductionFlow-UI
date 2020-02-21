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
            if (len(label_extr[key+1]) > len(val)):
                wc_leader_arr.append(1)
            else:
                wc_leader_arr.append(0)

    file['Leader'] = wc_leader_arr
    neo4j_map['Leader'] = wc_leader_arr
    # print(file.head())
    parent_label = []
    childe_label = []
    current_label = ""

    for key,val in enumerate(label_extr):
        if key == 0:
            cypher_creater += f'CREATE (:Gaszähler {{name: {val}, processname: {neo4j_map["Name"][key][key]}}}),'
            parent_label.append(val)
            childe_label.append(label_extr[key+1])
            current_label = val
        elif (key == len(label_extr)-1):
            cypher_creater += f' (:Gaszähler {{name: {val}, processname: {neo4j_map["Name"][0][key]}}})'
            # For last node the realtionship will be pointed to itself even though it's a leader WC
            if neo4j_map['Leader'][key] == 1:
                parent_label.append(val)
                childe_label.append(val)
            elif neo4j_map['Leader'][key] == 0:
                parent_label.append(val)
                childe_label.append(val)

        else:
            cypher_creater += f' (:Gaszähler {{name: {val}, processname: {neo4j_map["Name"][0][key]}}}),'
            if ((neo4j_map['Leader'][key] == 1) and (len(val) <= len(label_extr[key+1]))):
                parent_label.append(val)
                childe_label.append(label_extr[key+1])
                current_label = val
            elif ((neo4j_map['Leader'][key] == 1) and (len(val) >= len(label_extr[key+1]))):
                parent_label.append(val)
                childe_label.append(val)
                current_label = val
            elif neo4j_map['Leader'][key] == 0:
                parent_label.append(current_label)
                childe_label.append(val)

    print(cypher_creater)
    file['Parent'] = parent_label
    file['Child'] = childe_label
    print(file.head())
    file.to_csv('updated_wc_sap.csv',encoding='utf-8-sig',sep=';',index=False)

if __name__ == "__main__":
    runpg()
