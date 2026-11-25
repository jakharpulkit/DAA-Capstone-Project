def sample_graph():
    edges=[('Aarav','Diya'),('Aarav','Kabir'),('Aarav','Meera'),('Diya','Kabir'),('Diya','Ishaan'),('Kabir','Meera'),('Kabir','Riya'),('Meera','Riya'),('Ishaan','Riya'),('Ishaan','Neha'),('Riya','Neha'),('Neha','Arjun'),('Arjun','Zoya'),('Zoya','Kabir')]
    graph={}
    for a,b in edges:
        graph.setdefault(a,set()).add(b); graph.setdefault(b,set()).add(a)
    return {k:sorted(v) for k,v in graph.items()}
