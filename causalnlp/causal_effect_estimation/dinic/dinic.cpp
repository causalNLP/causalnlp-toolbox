#include<bits/stdc++.h>
#define M 10000000
#define N 1000000
#define INF 1000000000
#define int long long
#define ll long long
using namespace std;
inline ll read(){
    char c=getchar();while (c!='-'&&(c<'0'||c>'9'))c=getchar();
    ll k=0,kk=1;if (c=='-')c=getchar(),kk=-1;
    while (c>='0'&&c<='9')k=k*10+c-'0',c=getchar();return kk*k;
}using namespace std;
void write(ll x){if (x<0)x=-x,putchar('-');if (x/10)write(x/10);putchar(x%10+'0');}
void writeln(ll x){write(x);puts("");}
namespace Dinic {
    struct edge {
        int from, to, cap, flow;
    };
    edge edges[2 * M];
    vector<int> E[M];
    int dis[N], Q[N], cur[M];
    bool vis[N];
    int edge_cnt;

    void add_edge(int u, int v, int c) {
        edges[edge_cnt] = (edge) {u, v, c, 0};
        E[u].push_back(edge_cnt++);
        edges[edge_cnt] = (edge) {v, u, 0, 0};
        E[v].push_back(edge_cnt++);
    }

    void clear() {
        for (int i = 0; i < edge_cnt; ++i) {
            edges[i].flow = 0;
        }
    }

    bool BFS(int S, int T, int n) {
        int head = 0, tail = 0;
        for (int i = 1; i <= n; ++i) {
            vis[i] = false;
        }
        dis[T] = 0;
        vis[T] = true;
        Q[tail++] = T;
        while (head < tail) {
            int u = Q[head++];
            for (int i = 0; i < (int) E[u].size(); ++i) {
                edge e = edges[E[u][i] ^ 1];
                if (e.flow < e.cap && !vis[e.from]) {
                    vis[e.from] = true;
                    dis[e.from] = dis[u] + 1;
                    Q[tail++] = e.from;
                }
            }
        }
        return vis[S];
    }

    int DFS(int u, int T, int a) {
        if (u == T)
            return a;
        int m = a;
        for (int &i = cur[u]; i < (int) E[u].size(); ++i) {
            edge &e = edges[E[u][i]];
            if (e.flow < e.cap && vis[e.to] && dis[e.to] == dis[u] - 1) {
                int f = DFS(e.to, T, min(a, e.cap - e.flow));
                e.flow += f;
                edges[E[u][i] ^ 1].flow -= f;
                a -= f;
                if (a == 0)
                    break;
            }
        }
        return m - a;
    }

    long long max_flow(int S, int T, int n) {
        long long flow = 0;
        while (BFS(S, T, n)) {
            for (int i = 1; i <= n; ++i) {
                cur[i] = 0;
            }
            flow += DFS(S, T, INF);
        }
        return flow;
    }

    void print_edge(int n1, int m){
        int sum = 0;
        for (int i = 0;i < m*2; i += 2){
            if (edges[i].flow==1){
                sum+=1;
                write(edges[i].from-2);
                putchar(' ');
                writeln(edges[i].to-2-n1);
            }
        }
        //writeln(sum);
        //writeln(m);
    }
}
signed main(){
    //freopen("/cluster/project/sachan/zhiheng/MT_Causality/intermediate_data/fr-es.in", "r", stdin);
    int n1 = 250000, n2=250000, S=1, T=2;
    int m = read();
    for (int i = 1; i <= m; i++){
        int x = read()+2,y = read()+2+n1;
        Dinic::add_edge(x, y, 1);
    }
    for (int i = 1; i <= n1; i++){
        Dinic::add_edge(S, i+2, 1);
    }
    for (int i = 1; i <= n2; i++){
        Dinic::add_edge(i+2+n1, T, 1);
    }
    Dinic::max_flow(S, T, n1+n2+2);
//    freopen("fr-es.out","w",stdout);
    Dinic::print_edge(n1, m);
}


