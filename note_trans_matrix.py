import networkx as nx

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Catch-All/scale_degree_trans.dot")

H = [[0 for i in range(12)] for j in range(12)]
H_notes = [0]*12

for j in range(12):
  jstr = str(j)
  for k in range(12):
    kstr = str(k)
    try:
      H[j][k] = len(G[jstr][kstr])
      H_notes[j]+= len(G[jstr][kstr])
      H_notes[k]+= len(G[jstr][kstr])
    except:
      pass

opt_abs = True

if not opt_abs:
  for i in range(12):
    tmp_tot = 0
    for j in range(12):
      tmp_tot += H[i][j]
    for j in range(12):
      if tmp_tot > 0:
        H[i][j] *= 1.0/float(tmp_tot)
      else:
        H[i][j] = 0
        
       

for i in range(12):
  for j in range(12):
    print str(i)+' '+str(j)+' '+str(H[i][j])+' '+str(H_notes[i]*H_notes[j]/float(sum(H_notes)))



