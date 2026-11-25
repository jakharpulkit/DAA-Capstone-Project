from collections import deque
from time import perf_counter

def bfs(graph, start):
    if start not in graph: return []
    seen, order = {start}, []
    q = deque([start])
    while q:
        node = q.popleft(); order.append(node)
        for nxt in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt); q.append(nxt)
    return order

def dfs(graph, start):
    if start not in graph: return []
    seen, order, stack = set(), [], [start]
    while stack:
        node = stack.pop()
        if node in seen: continue
        seen.add(node); order.append(node)
        stack.extend(reversed(graph.get(node, [])))
    return order

def shortest_path(graph, source, target):
    if source not in graph or target not in graph: return None
    q, parent = deque([source]), {source: None}
    while q:
        node=q.popleft()
        if node==target:
            path=[]; cur=target
            while cur is not None: path.append(cur); cur=parent[cur]
            return path[::-1]
        for nxt in graph.get(node, []):
            if nxt not in parent: parent[nxt]=node; q.append(nxt)
    return None

def mutual_friends(graph, a, b):
    if a not in graph or b not in graph: return []
    return sorted(set(graph[a]) & set(graph[b]))

def recommend_friends(graph, user, limit=5):
    if user not in graph: return []
    excluded=set(graph[user]) | {user}; scores={}
    for friend in graph[user]:
        for candidate in graph.get(friend, []):
            if candidate not in excluded: scores[candidate]=scores.get(candidate,0)+1
    return sorted(scores.items(), key=lambda item:(-item[1],item[0]))[:limit]

def benchmark(graph, start):
    out={}
    for name, fn in [('BFS',bfs),('DFS',dfs)]:
        t=perf_counter(); order=fn(graph,start); elapsed=(perf_counter()-t)*1000
        out[name]={'visited':len(order),'time_ms':elapsed,'order':order}
    return out
