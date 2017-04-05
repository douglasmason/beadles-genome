import networkx as nx

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/song-chord-dur.dot")

JL = dict()
PM = dict()

for i in G.nodes(data=True):
  if i[1].has_key('category') and i[1]['category'].replace('"','') == 'song':
    if i[1].has_key('author') and i[1]['author'].replace('"','') == 'John Lennon':
      for j in G.neighbors(i[0]):
        try:
          JL[j] += float(G[i[0]][j][0]['weight'])
        except:
          JL[j] = float(G[i[0]][j][0]['weight'])
  if i[1].has_key('category') and i[1]['category'].replace('"','') == 'song':
    if i[1].has_key('author') and i[1]['author'].replace('"','') == 'Paul McCartney':
      for j in G.neighbors(i[0]):
        try:
          PM[j] += float(G[i[0]][j][0]['weight'])
        except:
          PM[j] = float(G[i[0]][j][0]['weight'])
  if i[1].has_key('category') and i[1]['category'].replace('"','') == 'song':
    if i[1].has_key('author') and i[1]['author'].replace('"','') == 'Lennon/McCartney':
      for j in G.neighbors(i[0]):
        try:
          JL[j] += float(G[i[0]][j][0]['weight'])
        except:
          JL[j] = float(G[i[0]][j][0]['weight'])
        try:
          PM[j] += float(G[i[0]][j][0]['weight'])
        except:
          PM[j] = float(G[i[0]][j][0]['weight'])


tot_JL = 0
for i in JL:
  tot_JL += JL[i]

  
tot_PM = 0
for i in PM:
  tot_PM += PM[i]
  

for i in JL:
  JL[i] *= 1.0/tot_JL


for i in PM:
  PM[i] *= 1.0/tot_PM


print '"I" '+str(JL['I'])+' '+str(PM['I'])
print '"V" '+str(JL['V'])+' '+str(PM['V'])
print '"IV" '+str(JL['IV'])+' '+str(PM['IV'])
print '"III" '+str(JL['III'])+' '+str(PM['III'])
print '"II" '+str(JL['II'])+' '+str(PM['II'])
print '"VI" '+str(JL['VI'])+' '+str(PM['II'])
print '"bVII" '+str(JL['bVII'])+' '+str(PM['bVII'])
print '"bVI" '+str(JL['bVI'])+' '+str(PM['bVI'])
print '"bIII" '+str(JL['bIII'])+' '+str(PM['bIII'])
print '"iv" '+str(JL['v'])+' '+str(PM['v'])
print '"iv" '+str(JL['iv'])+' '+str(PM['iv'])



