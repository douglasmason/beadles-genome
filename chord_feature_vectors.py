import networkx as nx
import numpy as np
import rpy2.robjects as robj
r = robj.r
#r.X11()

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/song-chord-dur.dot")

chordnames = ["I","i","II","ii","bIII","III","iii","IV","iv","V","v","bVI","VI","vi","bVII","VII","vii"]
chordnames = ["I","i","II","ii","bIII","iii","IV","iv","V","v","bVI","VI","vi","bVII",]
songnames = []
song_chord = []

for i in G.nodes(data=True):
  if i[1].has_key('category') and i[1]['category'].replace('"','') == 'song':  
    tmp_chords = [0.0]*len(chordnames)
    for j in G.neighbors(i[0]):         
      try:
          chord_ind = [ind for ind in range(len(chordnames)) if chordnames[ind]==j][0]
          tmp_chords[chord_ind] = float(G[i[0]][j][0]['weight']) 
      except:
          pass #tmp_chords[[i for i in range(len(chordnames)) if chordname_to_index[i]=="other"][0]] += float(G[i[0]][j][0]['weight'])
    if sum(tmp_chords) > 0.0:
        song_chord.append(tmp_chords)
        songnames.append(i[0])


for i in range(len(songnames)):
  if len(songnames[i])>30:
    songnames[i] = songnames[i][:30]+'...'
  j = songnames[i].find('(song)')
  if j>-1:
    songnames[i] = songnames[i][:j]+songnames[i][j+6:]

from rpy2.robjects.packages import importr
import copy
grdevices = importr('grDevices')
grdevices.png(file="/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/chords.png", width=5000, height=5000,res=400)

song_chord_array = np.array(song_chord).transpose()
sca = copy.copy(song_chord_array)
sca_sum = np.tile(np.sum(sca,0),(len(sca),1))
sca /= sca_sum
sca_average = np.tile(np.average(sca,1),(len(sca[0]),1))
#sca = (sca.transpose()-sca_average).transpose() #Use this line to get positive and negative values
sca /= sca_average.transpose()
#song_chord_array = np.power(np.array(song_chord).transpose(),0.2)
rvec = robj.FloatVector(sca.reshape(song_chord_array.size)) 
nc, nr = song_chord_array.shape
song_chord_r = r.matrix(rvec, nrow=nr, ncol=nc)
song_range = range(len(songnames))
r.library("gplots")
hm2 = r('heatmap.2')
hm2(song_chord_r.rx(robj.IntVector(song_range),True),labRow=songnames,labCol=chordnames,scale="row",margins=robj.FloatVector([3,30]),col=r('redgreen(75)'),trace="none",keysize=1,key="none")

grdevices.dev_off()


#from hcluster import pdist, linkage, dendrogram
#import numpy as np
#X = np.array(song_chord)
#X = X.transpose()
#Y = pdist(X)
#Z = linkage(Y)
#dendrogram(Z)
