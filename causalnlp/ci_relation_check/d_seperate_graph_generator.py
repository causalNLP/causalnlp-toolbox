from sample_graph import *
from icecream import ic

node_dict = {}
nodes = 0
def generate_graph(s, output_file = "graph.txt"):
    global node_dict, nodes
    def get_ids(node_name):
        global node_dict, nodes
        if (node_dict.get(node_name) == None):
            nodes += 1
            node_dict[node_name] = nodes
        return node_dict[node_name]
    edge_list = []
    hidden_variables = 0
    hidden_variables_list = []
    for i in s.split("\n"):
        if (len(i.split("->"))==1):
            continue
        if (len(i.split("<->"))==2):
            hidden_variables += 1
            fork_mediator = get_ids(f"hidden_variable_{hidden_variables}")
            hidden_variables_list.append(fork_mediator)
            hidden_variables += 1
            colider_mediator = get_ids(f"hidden_variable_{hidden_variables}")
            hidden_variables_list.append(colider_mediator)

            node_name1, node_name2 = i.split("<->")[0], i.split("<->")[1]
            node1_ids, node2_ids = get_ids(node_name1), get_ids(node_name2)
            edge_list.append([fork_mediator, node1_ids])
            edge_list.append([fork_mediator, node2_ids])
            edge_list.append([node1_ids, colider_mediator])
            edge_list.append([node2_ids, colider_mediator])
        else:
            node_name1, node_name2 = i.split("->")[0], i.split("->")[1]
            edge_list.append([get_ids(node_name1), get_ids(node_name2)])

    if (output_file == None):
        return node_dict, hidden_variables_list, nodes, edge_list
    else:
        with open(output_file, "w") as f:
            print(nodes, len(edge_list), file=f)
            for i in edge_list:
                print(i[0], i[1], file=f)
            print(hidden_variables, file=f)
            print(hidden_variables_list, file=f)
        #print(node_dict)
        return node_dict, hidden_variables_list

def generate_graph_str(causal_relation, corr_relation = None):
    node_dict = {}
    nodes = 0
    s = ""
    for i in causal_relation:
        if (node_dict.get(i[0]) == None):
            nodes += 1
            node_dict[i[0]] = nodes
        if (node_dict.get(i[1]) == None):
            nodes += 1
            node_dict[i[1]] = nodes
            s += f"{i[0]}->{i[1]}\n"
    if (corr_relation != None):
        for i in corr_relation:
            if (node_dict.get(i[0]) == None):
                nodes += 1
                node_dict[i[0]] = nodes
            if (node_dict.get(i[1]) == None):
                nodes += 1
                node_dict[i[1]] = nodes
                s += f"{i[0]}<->{i[1]}\n"
    return s

def run_code():
    import os
    os.system("g++ -std=c++11 -O3 -o d_seperate_graph d_seperate_graph.cpp")
    # run d_seperate_graph with graph.txt as input and output.txt as output
    os.system("./d_seperate_graph < graph.txt > output.txt")

def postProcess(node_dict, hidden_variavle_list):
    reversed_node_dict = {}
    for i in node_dict:
        reversed_node_dict[node_dict[i]-1] = i
    CI_list = []
    with open("output.txt", "r") as f:
        lines = f.readlines()
        x, y = 0, 0
        flag = False
        for i in lines:
            if "Condition set for" in i:
                x, y = i.split(" ")[-2], i.split(" ")[-1]
                flag = int(x) in hidden_variavle_list or int(y) in hidden_variavle_list
                x, y = reversed_node_dict[int(x)-1], reversed_node_dict[int(y)-1]
            else:
                if flag:
                    continue
                Z_binary = int(i)
                curr_node = 0
                z_list = []
                while Z_binary:
                    if Z_binary&1:
                        z_list.append(reversed_node_dict[curr_node])
                    Z_binary >>= 1
                    curr_node += 1
                CI_list.append([x, y, z_list])
    print(CI_list)
    return CI_list

def checkCI(x, y, z, CI_list = None, Graph = None):
    if CI_list == None:
        if Graph == None:
            raise Exception("Graph or CI_list must be provided")
        node_dict, hidden_variavle_list = generate_graph(Graph)
        run_code()
        CI_list = postProcess(node_dict, hidden_variavle_list)
    for i in CI_list:
        if (i[0]==x and i[1]==y and set(i[2])==set(z)):
            return True
    return False

if __name__ == '__main__':
    node_dict, hidden_variavle_list = generate_graph(sample_graph4)
    run_code()
    CI_list = postProcess(node_dict, hidden_variavle_list)