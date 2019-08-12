import os
import sys
import time
import shutil
import librosa
import numpy as np

sample_rate = int(sys.argv[2])
overrun_size = int(sys.argv[3]) # x % 60 seconds
file_list = list()

dirname_overrun = sys.argv[1]+'_overrun'

def searchFile(dirname): # for search files in directory
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_path = os.path.join(dirname, filename)
            if os.path.isdir(full_path):
                searchFile(full_path)
            else:
                ext = os.path.splitext(full_path)[-1]
                if ext == '.wav':
                    file_list.append(full_path)
    except Exception as e:
        print(e)
        #pass    

try: # make result directory
    os.mkdir(dirname_overrun)
except Exception as e:
    #print(e)
    pass

searchFile(sys.argv[1]) # file search
file_list.sort() # sort (by name)
#print(file_list) # show file list

target = np.zeros(overrun_size)
start = time.time()
while len(file_list) > 0: # loop until empty list
    wav = file_list[0] # get file name
    print('[Progress] : '+str(wav), end='')
    (file_dir, file_name) = os.path.split(wav) # path info(dir, name)
    #print('file dir:', file_dir)
    #print('file_name', file_name)

    data, rate = librosa.load(wav, sr=sample_rate) # open wav file

    # Check overrun
    take_snap = list()
    Slide = len(target)
    possibles = np.where(data == target[0])[0]
    for p in possibles:
      check = data[p:p+Slide]
      if np.all(check == target):
        take_snap.append(p)
    
    if len(take_snap) > 0:
        print(' >> [Alert] Overrun')
        shutil.move(wav, dirname_overrun+'/'+file_name)
    else:
        print(' >> [Success]')
    
    del(file_list[0])
    time.sleep(0)

# last file   
print('[Notice] Done')
print(time.time() - start)
