# SocialGraph — DAA Capstone Project 4

## Social Network Connection and Recommendation Analysis
A Streamlit-based social graph app representing users as vertices and friendships as undirected edges.

### Features
- Interactive graph visualization and network statistics
- BFS and DFS traversal exploration
- Shortest unweighted connection path using BFS
- Mutual-friend identification and recommendations ranked by shared connections
- Performance benchmarking on generated graph sizes with CSV export
- Add users and friendships interactively

### Run locally
Python 3.9+ recommended.
```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run src/app.py
```

### Tests
```bash
pytest -q
```

### Complexity
BFS, DFS, and shortest path: O(V + E) time and O(V) auxiliary space. Mutual friends: O(deg(u) + deg(v)). Recommendations: O(sum of degrees of the user's friends), O(V) worst-case space.

Graph representation: adjacency list; each friendship is stored in both directions. Benchmark results vary by hardware; repeat trials and use median/average for rigorous analysis.
