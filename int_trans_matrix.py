import networkx as nx

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Catch-All/interval_trans.dot")

H = [[0 for i in range(-25,25)] for j in range(-25,25)]

for j in range(-25,25):
  if j<0:
    jstr = 'n'+str(j)[1:]
  else:
    jstr = str(j)
  for k in range(-25,25):
    if k<0:
      kstr = 'n'+str(k)[1:]
    else:
      kstr = str(k)
    try:
      H[j][k] = len(G[jstr][kstr])
    except:
      pass

opt_abs = True

if not opt_abs:
  for i in range(-25,25):
    tmp_tot = 0
    for j in range(-25,25):
      tmp_tot += H[i][j]
    for j in range(-25,25):
      if tmp_tot > 0:
        H[i][j] *= 1.0/float(tmp_tot)
      else:
        H[i][j] = 0

for i in range(-25,25):
  for j in range(-25,25):
    print str(i)+' '+str(j)+' '+str(H[i][j])



