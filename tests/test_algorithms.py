from src.algorithms import bfs,dfs,shortest_path,mutual_friends,recommend_friends
from src.demo_data import sample_graph

def test_traversal_reaches_component():
    g=sample_graph(); assert set(bfs(g,'Aarav'))==set(g); assert set(dfs(g,'Aarav'))==set(g)
def test_shortest_path_edges():
    g=sample_graph();p=shortest_path(g,'Aarav','Neha');assert p[0]=='Aarav' and p[-1]=='Neha';assert all(p[i+1] in g[p[i]] for i in range(len(p)-1))
def test_mutual_friend_list():
    assert mutual_friends(sample_graph(),'Aarav','Diya')==['Kabir']
def test_recommendations_exclude_self_and_friends():
    g=sample_graph();r=dict(recommend_friends(g,'Aarav'));assert 'Aarav' not in r and not (set(r)&set(g['Aarav']))
