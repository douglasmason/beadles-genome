import networkx as nx
import numpy as np
import rpy2.robjects as robj
import copy
r = robj.r
#r.X11()

G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/scale_degree_trans.dot")

chordnames_all = ["1.0","1.5","2.0","2.5","3.0","3.5","4.0","4.5"]
chordnames = ["1.0","1.5","2.0","2.5","3.0","3.5","4.0","4.5"]
songnames = []
song_chord = []
prev_song = ''

#song_ind = [ind for ind in range(len(songnames)) if songnames[ind]==song][0]
#chord_ind = int(i[0])
for i in G.edges(data=True):
  if i[2].has_key('comment'):
    song = i[2]['comment']
    if not (song in songnames): 
        songnames.append(song)
        song_chord.append([0 for ind in range(len(chordnames))])
    song_ind = int((np.array(songnames)==song).nonzero()[0])
    beat = float(i[2]['second_beat'])
    chord = str(np.floor(beat) + ( 0.5 if np.mod(beat,1) else 0.0 ))
    try:
        chord_ind = [ind for ind in range(len(chordnames)) if chordnames[ind]==chord][0]
        song_chord[song_ind][chord_ind] += float(i[2]['dur']) #Weight by distance to prior note
        #song_chord[song_ind][chord_ind] += 1.0 #No weight
    except:
        pass

for i in range(len(songnames)):
  if len(songnames[i])>30:
    songnames[i] = songnames[i][:30]+'...'
  j = songnames[i].find('(song)')
  if j>-1:
    songnames[i] = songnames[i][:j]+songnames[i][j+6:]

from rpy2.robjects.packages import importr
import copy
grdevices = importr('grDevices')
grdevices.png(file="/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/beats.png", width=5000, height=5000,res=400)

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