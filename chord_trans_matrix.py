import networkx as nx

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Catch-All/chord_trans.dot")

H = [[0 for i in range(16)] for j in range(16)]
str_to_ind = ['']*15
str_to_ind[1] = "I"
str_to_ind[2] = "ii"
str_to_ind[3] = "iii"
str_to_ind[4] = "IV"
str_to_ind[5] = "V"
str_to_ind[6] = "vi"
str_to_ind[7] = "bVII"
str_to_ind[8] = "bVI"
str_to_ind[9] = "bIII"
str_to_ind[10] = "II"
str_to_ind[11] = "III"
str_to_ind[12] = "iv"
str_to_ind[13] = "v"
str_to_ind[14] = "i"

for j in range(len(str_to_ind)):
  for k in range(len(str_to_ind)):
    try:
      H[j][k] = len(G[str_to_ind[j]][str_to_ind[k]])
    except:
      pass

opt_abs = True

if not opt_abs:
  for i in range(1,len(H)):
    tmp_tot = 0
    for j in range(1,len(H[i])):
      tmp_tot += H[i][j]
    for j in range(1,len(H[i])):
      if not j==i:
        if tmp_tot > 0:
          H[i][j] *= 1.0/float(tmp_tot)
        else:
          H[i][j] = 0
      else:
        H[i][j] = 1

for i in range(len(H)):
  for j in range(len(H)):
    print str(i)+' '+str(j)+' '+str(H[i][j])



