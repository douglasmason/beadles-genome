import networkx as nx

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Catch-All/song-chord.dot")

rm_nodes = []
rm_edges = []

for i in G.nodes():
  rm_edges = []
  for j in G.neighbors(i):
    for k in range(G.number_of_edges(i,j)-1):
      rm_edges.append((i,j))
  G.remove_edges_from(rm_edges)
    


for i in G.nodes(data=True):
  if i[1].has_key('category') and i[1]['category'].replace('"','') == 'chord':
    rm_nodes.append(i[0])
    for j in G.neighbors(i[0]):
      for k in G.neighbors(i[0]):
        if j==k:
          continue
        G.add_edge(j,k,label=i[0])
        
        
G.remove_nodes_from(rm_nodes)
    
nx.write_dot(G,"/Volumes/Macintosh HD/Users/douglasmason/Documents/Catch-All/song-chord2.dot")
