import numpy as np
from icecream import ic
class CausalGraph(object):
    def __init__(self, n, edge_list, hidden_variable_list):
        #ic(n, edge_list, hidden_variable_list)
        self.all_path = []
        self.all_set = []
        self.n = n
        self.graph = np.zeros((n, n))
        self.decendents_x = [0]*self.n
        for edge in edge_list:
            self.graph[edge[0]-1][edge[1]-1] = 1
            self.graph[edge[1]-1][edge[0]-1] = -1
        self.hidden_variable_list = [i-1 for i in hidden_variable_list]

    def find_all_path(self, begin, end, current_path):
        # the graph here is a matrix
        # the end can be a node or a list of nodes
        if type(end)==int and begin == end or type(end)==list and begin in end:
            self.all_path.append(current_path)
            return
        for node in range(self.n):
            if self.graph[begin][node] != 0 and node not in current_path:
                self.find_all_path(node, end, current_path + [node])

    def find_all_set(self, current, current_set):
        if current == self.n:
            self.all_set.append(current_set)
            return
        self.find_all_set(current+1, current_set)
        self.find_all_set(current+1, current_set + [current])

    def find_decendent(self, current, blocked_set=[]):
        if self.decendents_x[current] != 0:
            return
        self.decendents_x[current] = 1
        for node in range(self.n):
            if node in blocked_set:
                continue
            if self.graph[current][node] == 1:
                self.find_decendent(node, blocked_set)

    def check_block_path(self, path, condition_set):
        # check if the path is blocked by the condition set, if it is blocked, return True, otherwise return False
        # first check if the begin node or end node is in the condition set, if so, then the path is blocked
        if path[0] in condition_set or path[-1] in condition_set:
            return True
        # then check all node in the path
        # for fork or chain node, if the node is in the condition set, then the path is blocked
        # for collider node, if the node is not in the condition set, then the path is blocked
        # otherwise, the path is not blocked
        for i in range(1, len(path)-1):
            if self.graph[path[i-1]][path[i]] == self.graph[path[i]][path[i+1]]:# chain node
                if path[i] in condition_set:
                    return True
            elif self.graph[path[i-1]][path[i]] == -1 and self.graph[path[i]][path[i+1]] == 1:# fork node
                if path[i] in condition_set:
                    return True
            elif self.graph[path[i-1]][path[i]] == 1 and self.graph[path[i]][path[i+1]] == -1:# collider node
                if path[i] not in condition_set:
                    return True
            else:
                ic(path, self.all_path, self.graph, i)
                raise Exception("The path is not valid")
        return False

    def generate_backdoor_set(self, treatment=None, effect=None):
        # return a list of backdoor set
        # 1. Z没有X的后代节点
        # 2. Z阻断了X和Y之间的所有指向X的路径（后门路径）
        self.all_set = []
        self.find_all_set(0, [])
        self.all_path = []
        self.find_all_path(treatment, effect, [treatment])
        self.decendents_x = [0] * self.n
        self.find_decendent(treatment)
        backdoor_set = []
        for condition_set in self.all_set:
            if treatment in condition_set or effect in condition_set:
                continue
            # check if the condition node in the decendent of treatment
            if any([self.decendents_x[i] == 1 for i in condition_set]):
                continue
            # check if hidden variable in the condition set
            if any([i in self.hidden_variable_list for i in condition_set]):
                continue
            for path in self.all_path:
                # if not the backdoor path, continue
                if self.graph[path[0]][path[1]] == 1:
                    continue
                if self.check_block_path(path, condition_set):
                    continue
                else:
                    break
            else:
                backdoor_set.append(condition_set)
        return backdoor_set

    def generate_all_backdoor_set(self):
        # return a dict of each two variable pair as (treatment, effect) and their backdoor set
        all_backdoor_set = {}
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    all_backdoor_set[(i, j)] = self.generate_backdoor_set(i, j)
        return all_backdoor_set

    def generate_frontdoor_set(self, treatment=None, effect=None):
        # 1. Z阻断了所有X到Y的有向路径
        # 2. X到Z没有后门路径
        # 3. Z到Y的后门路径都被X阻断
        self.all_set = []
        self.find_all_set(0, [])
        frontdoor_set = []
        #print(self.graph)
        #ic("begin of generate_frontdoor_set, the treatment is {}, the effect is {}".format(treatment, effect))
        for condition_set in self.all_set:
            if treatment in condition_set or effect in condition_set:
                continue
            # check if hidden variable in the condition set
            if any([i in self.hidden_variable_list for i in condition_set]):
                continue
            # check if the path from treatment to effect is blocked by condition set
            self.decendents_x = [0] * self.n
            self.find_decendent(treatment, condition_set)
            if self.decendents_x[effect] == 1:
                # this means the path from treatment to effect is not blocked by condition set
                #print("condition set is {}".format(condition_set))
                #print(self.decendents_x)
                continue
            #print("condition set is {}".format(condition_set))
            # condition 2: there is no backdoor path from treatment to condition set
            # Update: there is no un-blocked backdoor path from treatment to condition set
            self.all_path = []
            self.find_all_path(treatment, condition_set, [treatment])
            flag = False
            for path in self.all_path:
                if self.graph[path[0]][path[1]] == -1:
                    # this means the path is not a backdoor path
                    if not self.check_block_path(path, []):
                        break
            else:
                flag = True
            #ic(path)
            if not flag:
                continue
            #print("condition set is {}".format(condition_set))
            # condition 3: all backdoor path from condition set to effect is blocked by treatment
            self.all_path = []
            for node in condition_set:
                self.find_all_path(node, effect, [node])
            for path in self.all_path:
                if self.graph[path[0]][path[1]] == -1:
                    # this means the path is a backdoor path
                    if not self.check_block_path(path, [treatment]):
                        break
            else:
                frontdoor_set.append(condition_set)
                #print("condition set is {}".format(condition_set))
        #ic("end of generate_frontdoor_set, the treatment is {}, the effect is {}".format(treatment, effect))
        return frontdoor_set

    def generate_all_frontdoor_set(self):
        # return a dict of each two variable pair as (treatment, effect) and their frontdoor set
        all_frontdoor_set = {}
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    all_frontdoor_set[(i, j)] = self.generate_frontdoor_set(i, j)
        return all_frontdoor_set

def generate_all_backdoor_set(graph, treatment = None, effect = None):
    from d_seperate_graph_generator import generate_graph
    node_dict, hidden_variable_list, n, edge_list = generate_graph(graph, output_file = None)
    reversed_node_dict = {v:k for k, v in node_dict.items()}
    #ic(reversed_node_dict, node_dict, hidden_variable_list, n, edge_list)
    causal_graph = CausalGraph(n, edge_list, hidden_variable_list)
    if treatment == None and effect == None:
        backdoor_dict =  causal_graph.generate_all_backdoor_set()
        new_backdoor_dict = {}
        for key, value in backdoor_dict.items():# key is a tuple of (treatment, effect), value is a list of backdoor set
            new_backdoor_dict[(reversed_node_dict[key[0]+1], reversed_node_dict[key[1]+1])] = [[reversed_node_dict[i+1] for i in j] for j in value]
    else:
        backdoor_list = causal_graph.generate_backdoor_set(node_dict[treatment]-1, node_dict[effect]-1)
        new_backdoor_list = [[reversed_node_dict[i+1] for i in j] for j in backdoor_list]
        #ic(new_backdoor_list, treatment, effect, backdoor_list)
        #ic(causal_graph.graph, causal_graph.all_path, causal_graph.decendents_x)
        #ic(node_dict[treatment]-1, node_dict[effect]-1)
        return new_backdoor_list

def check_backdoor_set(graph, adjustment_set, treatment, effect):
    backdoor_set = generate_all_backdoor_set(graph, treatment, effect)
    adjustment_set = set(adjustment_set)
    backdoor_set = [set(i) for i in backdoor_set]
    if adjustment_set in backdoor_set:
        return True
    else:
        return False

def generate_all_frontdoor_set(graph, treatment = None, effect = None):
    from d_seperate_graph_generator import generate_graph
    node_dict, hidden_variable_list, n, edge_list = generate_graph(graph, output_file = None)
    reversed_node_dict = {v:k for k, v in node_dict.items()}
    #ic(reversed_node_dict, node_dict, hidden_variable_list, n, edge_list)
    causal_graph = CausalGraph(n, edge_list, hidden_variable_list)
    if treatment == None and effect == None:
        frontdoor_dict =  causal_graph.generate_all_frontdoor_set()
        new_frontdoor_dict = {}
        for key, value in frontdoor_dict.items():
            new_frontdoor_dict[(reversed_node_dict[key[0]+1], reversed_node_dict[key[1]+1])] = [[reversed_node_dict[i+1] for i in j] for j in value]
    else:
        frontdoor_list = causal_graph.generate_frontdoor_set(node_dict[treatment]-1, node_dict[effect]-1)
        new_frontdoor_list = [[reversed_node_dict[i+1] for i in j] for j in frontdoor_list]
        #ic(new_frontdoor_list, treatment, effect, frontdoor_list)
        #ic(causal_graph.graph, causal_graph.all_path, causal_graph.decendents_x)
        #ic(node_dict[treatment]-1, node_dict[effect]-1)
        return new_frontdoor_list

def check_frontdoor_set(graph, adjustment_set, treatment, effect):
    frontdoor_set = generate_all_frontdoor_set(graph, treatment, effect)
    adjustment_set = set(adjustment_set)
    frontdoor_set = [set(i) for i in frontdoor_set]
    if adjustment_set in frontdoor_set:
        return True
    else:
        return False

if __name__ == "__main__":
    from sample_graph import *
    from d_seperate_graph_generator import generate_graph
    ic(generate_all_frontdoor_set(sample_graph10, treatment = "x", effect = "y"))


