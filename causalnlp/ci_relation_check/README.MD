# CI relation check

#### Current C++ code is not correct
#### TODO: fix C++ code
#### TODO: make more accessible as a package

## How to use
### convection on causal graph (str format)
Our causal graph is represented by a string, where each line is a edge in graph, and is represented by a string of the form `node_name1->node_name2`. 
* causal link: `X->Y`, X is the cause of Y
* correlation link: `X<->Y`, X and Y are correlated

For example, the causal graph in the figure below is represented by the string
```
env->X_1
env->Y
X_1->Y
X_1->X_2
```
There is also a function to translate a causal graph from the list of causal/corr edges to the string format.

```python
def generate_graph_str(causal_relation, corr_relation = None)
```

### functions to execute CI
(1) for causal_graph to all_Ind_relations,
```python
def calcAllCI(Graph)
```

(2) given a causal_graph, x_variable_index, y_variable_index, check whether an adjustment set Z_set is a valid backdoor adjustment set for X->Y (here, we want to get the ACE of X on Y, and need to check if Z is correct to adjust for when using backdoor adjustment)

```python
def checkCI(x, y, z, CI_list = None, Graph = None)
```