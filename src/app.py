import random
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from algorithms import bfs, dfs, shortest_path, mutual_friends, recommend_friends, benchmark
from demo_data import sample_graph

st.set_page_config(page_title='SocialGraph | DAA Capstone', page_icon='🕸️', layout='wide')
st.title('🕸️ SocialGraph')
st.caption('Social Network Connection & Recommendation Analysis | DAA Capstone')
if 'graph' not in st.session_state: st.session_state.graph=sample_graph()
g=st.session_state.graph; users=sorted(g)
st.sidebar.header('Network Controls')
if st.sidebar.button('Reset demo network'):
    st.session_state.graph=sample_graph(); st.rerun()
with st.sidebar.expander('Add user'):
    name=st.text_input('Name')
    links=st.multiselect('Connect to',users)
    if st.button('Add user'):
        name=name.strip()
        if name and name not in g:
            g[name]=[]
            for f in links: g[name].append(f); g[f].append(name); g[f].sort()
            st.rerun()
        else: st.warning('Enter a new name.')
with st.sidebar.expander('Add friendship'):
    a=st.selectbox('First user',users,key='add_a'); b=st.selectbox('Second user',users,key='add_b')
    if st.button('Create connection'):
        if a!=b and b not in g[a]: g[a].append(b); g[b].append(a); g[a].sort();g[b].sort();st.rerun()
G=nx.Graph(g)
c1,c2,c3,c4=st.columns(4)
c1.metric('Users',G.number_of_nodes());c2.metric('Friendships',G.number_of_edges());c3.metric('Density',f'{nx.density(G):.1%}');c4.metric('Connected components',nx.number_connected_components(G))
tabs=st.tabs(['Network map','BFS / DFS','Shortest path','Mutual friends','Recommendations','Performance lab'])
with tabs[0]:
    fig,ax=plt.subplots(figsize=(10,6)); pos=nx.spring_layout(G,seed=42)
    nx.draw_networkx(G,pos,ax=ax,node_color='#8ecae6',edge_color='#adb5bd',node_size=1500,font_size=9,with_labels=True);ax.axis('off');st.pyplot(fig)
    st.caption('Vertices are people; undirected edges represent friendships.')
with tabs[1]:
    start=st.selectbox('Starting user',users); alg=st.radio('Algorithm',['BFS','DFS'],horizontal=True)
    order=bfs(g,start) if alg=='BFS' else dfs(g,start)
    st.subheader('Traversal order');st.code(' → '.join(order));st.write(f'{alg} visited {len(order)} reachable vertices.')
    st.info('BFS explores level by level using a queue. DFS follows a branch using a stack, then backtracks.')
with tabs[2]:
    source=st.selectbox('From',users,key='source');target=st.selectbox('To',users,key='target')
    if source==target: st.info('Choose two different users.')
    else:
        path=shortest_path(g,source,target)
        if path: st.success(f'{len(path)-1} connection hop(s)');st.markdown(' → '.join(f'**{p}**' for p in path));st.write('Degrees of separation:',len(path)-1)
        else: st.warning('No connection path found.')
with tabs[3]:
    x=st.selectbox('User A',users,key='mut_a');y=st.selectbox('User B',users,key='mut_b')
    mutual=mutual_friends(g,x,y) if x!=y else []
    st.metric('Mutual friends',len(mutual));st.write(', '.join(mutual) if mutual else 'No mutual connections.')
with tabs[4]:
    person=st.selectbox('Recommend for',users,key='rec_user');recs=recommend_friends(g,person)
    if recs: st.dataframe(pd.DataFrame(recs,columns=['Suggested user','Mutual friend count']),hide_index=True,use_container_width=True)
    else: st.info('No suggestions for this user.')
    st.caption('Recommendations are ranked by mutual-friend count; current friends and self are excluded.')
with tabs[5]:
    sizes=st.multiselect('Graph sizes (vertices)',[100,500,1000,2500,5000],default=[100,500,1000]);p=st.slider('Edge probability',0.001,0.05,0.01,0.001)
    if st.button('Run BFS / DFS benchmark'):
        rows=[]
        for n in sizes:
            rng=random.Random(42+n); test={str(i):[] for i in range(n)}
            for i in range(n):
                for j in range(i+1,n):
                    if rng.random()<p: test[str(i)].append(str(j));test[str(j)].append(str(i))
            result=benchmark(test,'0')
            for alg,result_data in result.items(): rows.append({'Vertices':n,'Edges':sum(map(len,test.values()))//2,'Algorithm':alg,'Visited':result_data['visited'],'Time (ms)':result_data['time_ms']})
        df=pd.DataFrame(rows);st.dataframe(df,hide_index=True,use_container_width=True)
        fig,ax=plt.subplots()
        for alg in df.Algorithm.unique():
            d=df[df.Algorithm==alg];ax.plot(d.Vertices,d['Time (ms)'],marker='o',label=alg)
        ax.set_xlabel('Vertices');ax.set_ylabel('Runtime (ms)');ax.set_title('BFS vs DFS runtime');ax.grid(alpha=.3);ax.legend();st.pyplot(fig)
        st.download_button('Download results CSV',df.to_csv(index=False),'benchmark_results.csv','text/csv')
        st.caption('Benchmark times vary by hardware and load. Repeat trials and report average/median for formal analysis.')
st.divider();st.subheader('Complexity analysis')
st.markdown('| Algorithm | Time complexity | Auxiliary space |\n|---|---|---|\n| BFS | O(V + E) | O(V) |\n| DFS | O(V + E) | O(V) |\n| Shortest path (BFS) | O(V + E) | O(V) |\n| Mutual friends | O(deg(u) + deg(v)) | O(min degree) |\n| Recommendations | O(sum of friends’ degrees) | O(V) worst case |')
