sample_graph1 = """
u2->w
u2->i
u1->w
u1->e
w->z
z->e
e->i
u3->s
u3->w
s->z
s->e
s->i
g->z
g->e
g->i
"""
sample_graph2 = """
X_indZ->Y
X_YnZ->Y
Z->X_YnZ
Z->X_indY
Z--Y
"""
sample_graph3 = """
Y->X_indZ
Y->X_YnZ
Z->X_YnZ
Z->X_indY
Z<->Y
"""
sample_graph4 = """
env->X_1
env->Y
X_1->Y
X_1->X_2
"""
sample_graph5 = """
x->y
y->z
"""
sample_graph6 = """
x->y
z->y
"""

sample_graph7 = """
x->mediator
mediator->y
confounder->y
confounder->x
"""

sample_graph8 = """
x->mediator
mediator->y
confounder1->y
confounder2->x
confounder1->confounder2
"""

sample_graph8 = """
x->mediator
mediator->y
confounder1->y
confounder2->x
confounder1->confounder2
"""

sample_graph9 = """
x->mediator
mediator->y
confounder1->y
confounder2->x
confounder1->confounder3
confounder2->confounder3
"""

sample_graph10 = """
x->mediator1
x->mediator2
mediator1->mediator3
mediator2->mediator3
mediator3->y
confounder->y
confounder->x
"""