#include <iostream>
#include <cstdio>
#include <algorithm>
#include <map>
#define ll long long
#define int long long
inline ll read(){
    char c=getchar();while (c!='-'&&(c<'0'||c>'9'))c=getchar();
    ll k=0,kk=1;if (c=='-')c=getchar(),kk=-1;
    while (c>='0'&&c<='9')k=k*10+c-'0',c=getchar();return kk*k;
}using namespace std;
void write(ll x){if (x<0)x=-x,putchar('-');if (x/10)write(x/10);putchar(x%10+'0');}
void writeln(ll x){write(x);puts("");}
using namespace std;
int n, m, edge[110][110];
int path[10000010][2], path_num;
int num_hidden, hidden[110];

int evaluate_condition_set(int condition_nodes, int x, int y){
    if ((condition_nodes>>(x-1))&1 or (condition_nodes>>(y-1))&1)
        return 0;
    // We can not select hidden nodes
    for (int i = 1; i <= num_hidden; i++)
        if ((condition_nodes>>(hidden[i]-1))&1)
            return 0;
    for (int i = 1;i <= path_num; i++) {
        if (((condition_nodes&path[i][0])^path[i][1]))
            continue;
        return 0;
    }
    return 1;
}
int add_path(int select_nodes, int node_states){
    path_num++;
    path[path_num][0] = select_nodes;
    path[path_num][1] = node_states;
    return 0;
}
int find_all_paths(int current, int y, int select_nodes, int node_states, int last_states){
    //last_states: whether current point have input edge
    if (current == y){
        add_path(select_nodes, node_states);
        return 0;
    }
    for (int i = 1;i <= n; i++)
        if (((select_nodes>>(i-1))&1)==0 and (edge[current][i] or edge[i][current])){
            //write(current); putchar(' ');write(i);putchar(' ');writeln(node_states);
            int new_select_nodes = select_nodes|(1ll<<(i-1));
            if (edge[current][i]){
                find_all_paths(i, y, new_select_nodes, node_states,  1);
            }else{
                if (last_states == 1){
                    find_all_paths(i, y, new_select_nodes, node_states|(1ll<<(current-1)),  0);
                }else{
                    find_all_paths(i, y, new_select_nodes, node_states,  0);
                }
            }
        }
    return 0;
}
/*
 * 我们发现如果两个path需要的节点集合是一样的， 但是不同节点的状态不同；
 * 如果有一个节点状态不同的话， 异或就行了
 * 如果有多于一个节点状态不同， 感觉还是要都放进去？
 * 算了直接都放进去吧。。
 *
 * update:
 * 可以把整个算法优化到3^n
 *
 * 额外的剪枝:
 * 1. 只保留相关节点 (所有共同祖先和路径上节点)
 * 2. 如果我们只要判断所有单个节点？
 * 不管了先搓一个最简单的可用版本
 */
 int calculate_d_seperate(int x, int y){
    path_num = 0;
    find_all_paths(x, y, 1<<(x-1), 0, 0);
    //puts("Printing all paths");
    //writeln(path_num);
    //for (int i = 1; i <= path_num; i++){
    //    write(path[i][0]); putchar(' ');writeln(path[i][1]);
    //}
    //puts("Printing all condition set");
    for (int i = 0; i < (1<<n); i++){
        //cout<<i<<' '<<x<<' '<<y<<endl;
        if (evaluate_condition_set(i, x, y)){
            writeln(i);
        }
    }
    return 0;
}

signed main() {
    n = read();m = read();
    for (int i = 1; i <= m; i++) {
        int x = read(), y = read();
        edge[x][y] = 1;
    }
    num_hidden = read();
    for (int i = 1; i <= num_hidden; i++){
        hidden[i] = read();
    }

    for (int x = 1; x < n; x++)
        for (int y = x+1; y <= n; y++)
            if (x != y){
                printf("Condition set for %d %d\n", x, y);
                calculate_d_seperate(x, y);
            }
}
/*
7 8
1 2
1 3
4 3
4 5
6 4
6 1
4 7
1 7
2
[6, 7]
2 4

9 15
1 2
1 3
4 2
4 5
2 6
6 5
5 3
7 8
7 2
8 6
8 5
8 3
9 6
9 5
9 3
0

4 3
 1 3
 2 3
 3 4
 0
 1 2
 */