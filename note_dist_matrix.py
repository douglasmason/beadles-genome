import networkx as nx

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Catch-All/scale_degree_trans.dot")

H = [[0 for i in range(-12,13)] for j in range(12)]

opt_ante = False

for j in range(12):
  jstr = str(j)
  for k in range(12):
    kstr = str(k)
    try:
      for n in range(len(G[jstr][kstr])):
        dist = int(G[jstr][kstr][n]['dist'])
        if dist>12:
          dist = 12
        if dist<-12:
          dist = -12
        if opt_ante:
          H[j][dist] += 1
        else:
          H[k][dist] += 1
    except:
      pass


opt_abs = False

if not opt_abs:
  for i in range(12):
    tmp_tot = 0
    for j in range(-12,13):
      tmp_tot += H[i][j]
    for j in range(-12,13):
      if tmp_tot > 0:
        H[i][j] *= 1.0/float(tmp_tot)
      else:
        H[i][j] = 0

for i in range(12):
  for j in range(-12,13):
    print str(i)+' '+str(j)+' '+str(H[i][j])



