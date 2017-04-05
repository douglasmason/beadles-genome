import networkx as nx, math

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Catch-All/scale_degree_trans.dot")

max_dur = 5
H = [[0 for i in range(max_dur*2+1)] for j in range(-12,13)]
H_dur = [0]*(max_dur*2+1)
H_int = [0]*(13+12)

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
        dur = float(G[jstr][kstr][n]['dur'])
        if dur>max_dur:
          dur = max_dur
        if dur == 0:
          continue
        H[dist][int(dur*2)] += 1
        H_dur[int(dur*2)]+=1
        H_int[dist] += 1
        
    except:
      pass


total = 0
for tmp in H_dur:
  total += tmp

opt_abs = True

if not opt_abs:
  for i in range(-12,13):
    tmp_tot = 0
    for j in range(max_dur*2+1):
      tmp_tot += H[i][j]
    for j in range(max_dur*2+1):
      if tmp_tot > 0:
        H[i][j] *= 1.0/float(tmp_tot)
      else:
        H[i][j] = 0

for i in range(-12,13):
  for j in range(max_dur*2+1):
    print str(i)+' '+str(j/2.0)+' '+str(H[i][j])+' '+str(H_dur[j]*H_int[i]/float(total))



