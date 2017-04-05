import networkx as nx
import numpy as np
import rpy2.robjects as robj
r = robj.r
#r.X11()


H = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/song-chord-dur.dot")
G = nx.read_dot("/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/scale_degree_trans.dot")

#######
# Chord
#######

chordnames = ["I","i","II","ii","bIII","III","iii","IV","iv","V","v","bVI","VI","vi","bVII","VII","vii"]
chordnames = ["I","i","II","ii","bIII","iii","IV","iv","V","v","bVI","VI","vi","bVII",]
songnames = []
song_chord = []

for i in H.nodes(data=True):
  if i[1].has_key('category') and i[1]['category'].replace('"','') == 'song':  
    tmp_chords = [0.0]*len(chordnames)
    for j in H.neighbors(i[0]):         
      try:
          chord_ind = [ind for ind in range(len(chordnames)) if chordnames[ind]==j][0]
          tmp_chords[chord_ind] = float(H[i[0]][j][0]['weight']) 
      except:
          pass #tmp_chords[[i for i in range(len(chordnames)) if chordname_to_index[i]=="other"][0]] += float(G[i[0]][j][0]['weight'])
    if sum(tmp_chords) > 0.0:
        song_chord.append(tmp_chords)
        songnames.append(i[0])


song_chord_array = np.array(song_chord).transpose()
sca = copy.copy(song_chord_array)
sca_sum = np.tile(np.sum(sca,0),(len(sca),1))
sca /= sca_sum
sca_average = np.tile(np.average(sca,1),(len(sca[0]),1))
#sca = (sca.transpose()-sca_average).transpose() #Use this line to get positive and negative values
sca /= sca_average.transpose()
#song_chord_array = np.power(np.array(song_chord).transpose(),0.2)

######
# Note
######


notenames_all = ["1","b2","2","b3","3","4","b5","5","b6","6","b7","7"]
#notenames = ["1","b2","2","b3","3","4","b5","5","b6","6","b7","7"]
notenames = ["1","2","b3","3","4","5","6","b7","7"]
song_note = [[0 for i in range(len(notenames))] for j in range(len(songnames))]
prev_song = ''

#song_ind = [ind for ind in range(len(songnames)) if songnames[ind]==song][0]
#note_ind = int(i[0])
for i in G.edges(data=True):
  if i[2].has_key('comment'):
    song = i[2]['comment']
    if not (song in songnames):
      continue
    song_ind = int((np.array(songnames)==song).nonzero()[0])
    try:
        note_ind = [ind for ind in range(len(notenames)) if notenames[ind]==notenames_all[int(i[0])]][0]
        song_note[song_ind][note_ind] += float(i[2]['dur'])
    except:
        pass


song_note_array = np.array(song_note).transpose()
sna = copy.copy(song_note_array)
sna_sum = np.tile(np.sum(sna,0),(len(sna),1))
sna /= sna_sum
sna_average = np.tile(np.average(sna,1),(len(sna[0]),1))
#sna = (sna.transpose()-sna_average).transpose() #Use this line to get positive and negative values
sna /= sna_average.transpose()
#song_note_array = np.power(np.array(song_note).transpose(),0.2)

######
# Beat
######

beatnames_all = ["1.0","1.5","2.0","2.5","3.0","3.5","4.0","4.5"]
beatnames = ["1.0","1.5","2.0","2.5","3.0","3.5","4.0","4.5"]
song_beat = [[0 for i in range(len(beatnames))] for j in range(len(songnames))]
prev_song = ''

#song_ind = [ind for ind in range(len(songnames)) if songnames[ind]==song][0]
#beat_ind = int(i[0])
for i in G.edges(data=True):
  if i[2].has_key('comment'):
    song = i[2]['comment']
    if not (song in songnames):
      continue
    song_ind = int((np.array(songnames)==song).nonzero()[0])
    beat = float(i[2]['second_beat'])
    simpler_beat = str(np.floor(beat) + ( 0.5 if np.mod(beat,1) else 0.0 ))
    try:
        beat_ind = [ind for ind in range(len(beatnames)) if beatnames[ind]==simpler_beat][0]
        song_beat[song_ind][beat_ind] += float(i[2]['dur']) #Weight by distance to prior note
        #song_beat[song_ind][beat_ind] += 1.0 #No weight
    except:
        pass


song_beat_array = np.array(song_beat).transpose()
sba = copy.copy(song_beat_array)
sba_sum = np.tile(np.sum(sba,0),(len(sba),1))
sba /= sba_sum
sba_average = np.tile(np.average(sba,1),(len(sba[0]),1))
#sba = (sba.transpose()-sba_average).transpose() #Use this line to get positive and negative values
sba /= sba_average.transpose()
#song_beat_array = np.power(np.array(song_beat).transpose(),0.2)

######
# Process for R
######

for i in range(len(songnames)):
  if len(songnames[i])>30:
    songnames[i] = songnames[i][:30]+'...'
  j = songnames[i].find('(song)')
  if j>-1:
    songnames[i] = songnames[i][:j]+songnames[i][j+6:]


from rpy2.robjects.packages import importr
import copy
grdevices = importr('grDevices')
grdevices.png(file="/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/all.png", width=5000, height=5000,res=400)

all_array = np.concatenate((sca,sna,sba))
allnames = chordnames+notenames+beatnames

rvec = robj.FloatVector(all_array.reshape(all_array.size)) 
nc, nr = all_array.shape
all_array_r = r.matrix(rvec, nrow=nr, ncol=nc)
song_range = range(len(songnames))
r.library("gplots")
hm2 = r('heatmap.2')
hm2(all_array_r.rx(robj.IntVector(song_range),True),labRow=songnames,labCol=allnames,scale="row",margins=robj.FloatVector([3,15]),col=r('redgreen(75)'),trace="none",keysize=1)

grdevices.dev_off()


from rpy2.robjects.packages import importr
import copy
grdevices = importr('grDevices')
grdevices.png(file="/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/chord_note.png", width=5000, height=5000,res=400)

all_array = np.dot(sna,sca.transpose())

rvec = robj.FloatVector(all_array.reshape(all_array.size)) 
nc, nr = all_array.shape
all_array_r = r.matrix(rvec, nrow=nr, ncol=nc)
r.library("gplots")
hm2 = r('heatmap.2')
hm2(all_array_r,labRow=chordnames,labCol=notenames,scale="col",margins=robj.FloatVector([3,15]),col=r('redgreen(75)'),trace="none",keysize=1)

grdevices.dev_off()



from rpy2.robjects.packages import importr
import copy
grdevices = importr('grDevices')
grdevices.png(file="/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/chord_beat.png", width=5000, height=5000,res=400)

all_array = np.dot(sba,sca.transpose())

rvec = robj.FloatVector(all_array.reshape(all_array.size)) 
nc, nr = all_array.shape
all_array_r = r.matrix(rvec, nrow=nr, ncol=nc)
r.library("gplots")
hm2 = r('heatmap.2')
hm2(all_array_r,labRow=chordnames,labCol=beatnames,scale="col",margins=robj.FloatVector([3,15]),col=r('redgreen(75)'),trace="none",keysize=1)

grdevices.dev_off()



from rpy2.robjects.packages import importr
import copy
grdevices = importr('grDevices')
grdevices.png(file="/Volumes/Macintosh HD/Users/douglasmason/Documents/Insight/Beatles/note_beat.png", width=5000, height=5000,res=400)

all_array = np.dot(sna,sba.transpose())

rvec = robj.FloatVector(all_array.reshape(all_array.size)) 
nc, nr = all_array.shape
all_array_r = r.matrix(rvec, nrow=nr, ncol=nc)
r.library("gplots")
hm2 = r('heatmap.2')
hm2(all_array_r,labRow=beatnames,labCol=notenames,scale="row",margins=robj.FloatVector([3,15]),col=r('redgreen(75)'),trace="none",keysize=1)

grdevices.dev_off()