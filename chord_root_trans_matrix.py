import networkx as nx

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Catch-All/chord_trans.dot")

H_chords = [0]*12

H = [[0 for i in range(12)] for j in range(12)]
ind_to_ind = [0]*18
str_to_ind = ['']*18
str_to_ind[1] = "I"
ind_to_ind[1] = 0
str_to_ind[2] = "ii"
ind_to_ind[2] = 2
str_to_ind[3] = "iii"
ind_to_ind[3] = 4
str_to_ind[4] = "IV"
ind_to_ind[4] = 5
str_to_ind[5] = "V"
ind_to_ind[5] = 7
str_to_ind[6] = "vi"
ind_to_ind[6] = 9
str_to_ind[7] = "bVII"
ind_to_ind[7] = 10
str_to_ind[8] = "bVI"
ind_to_ind[8] = 8
str_to_ind[9] = "bIII"
ind_to_ind[9] = 3
str_to_ind[10] = "II"
ind_to_ind[10] = 2
str_to_ind[11] = "III"
ind_to_ind[11] = 4
str_to_ind[12] = "iv"
ind_to_ind[12] = 5
str_to_ind[13] = "v"
ind_to_ind[13] = 7
str_to_ind[14] = "i"
ind_to_ind[14] = 0
str_to_ind[15] = "bv"
ind_to_ind[15] = 6
str_to_ind[16] = "vii"
ind_to_ind[16] = 11
str_to_ind[17] = "VII"
ind_to_ind[17] = 11

for j in range(len(str_to_ind)):
  for k in range(len(str_to_ind)):
    try:
      H[ind_to_ind[j]][ind_to_ind[k]] += len(G[str_to_ind[j]][str_to_ind[k]])
      H_chords[ind_to_ind[j]] += len(G[str_to_ind[j]][str_to_ind[k]])
      H_chords[ind_to_ind[k]] += len(G[str_to_ind[j]][str_to_ind[k]])
    except:
      pass

opt_abs = True

if not opt_abs:
  for i in range(0,len(H)):
    tmp_tot = 0
    for j in range(0,len(H[i])):
      tmp_tot += H[i][j]
    for j in range(0,len(H[i])):
      if not j==i:
        if tmp_tot > 0:
          H[i][j] *= 1.0/float(tmp_tot)
        else:
          H[i][j] = 0
      else:
        H[i][j] = 1

for i in range(len(H)):
  for j in range(len(H)):
    print str(i)+' '+str(j)+' '+str(H[i][j])+' '+str(H_chords[i]*H_chords[j]/float(sum(H_chords)))



