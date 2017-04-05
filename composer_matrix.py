import networkx as nx

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Catch-All/song-chord.dot")

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


for i in G.nodes(data=True):
  if i[1].has_key('category') and i[1]['category'].replace('"','') == 'song':
    if i[1].has_key('author') and (i[1]['author'].replace('"','') == 'John Lennon' or  i[1]['author'].replace('"','') == 'Paul McCartney' or  i[1]['author'].replace('"','') == 'Lennon/McCartney'):
      for j in G.neighbors(i[0]):
        jind = 15
        for jtmp in range(len(str_to_ind)):
          if j==str_to_ind[jtmp]:
            jind = jtmp
        H[jind][0] += 1
        for k in G.neighbors(i[0]):
          kind = 15
          for ktmp in range(len(str_to_ind)):
            if k==str_to_ind[ktmp]:
              kind = ktmp
          H[jind][kind] += 1

opt_abs = True

if not opt_abs:
  for i in range(1,len(H)):
    tmp_tot = H[i][0]
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



