import os
import sys
import time
from datetime import datetime, timedelta

import librosa
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt


sample_rate = int(sys.argv[2]) # sample rate
defined_size = sample_rate * 60 # 1 minute
offset_size = int(sys.argv[3]) % defined_size # x % 60 seconds
file_list = list()
name_split = list()
time_info = None
data_buf = np.array([])

dirname_adjusted = sys.argv[1]+'_adjusted'

def viewGraph(name, data, sr, save, show): # for inspect data
    time = np.linspace(0, len(data)/sr, len(data))
    fig, axis = plt.subplots() # plot
    axis.plot(time, data, color='b', label=name)
    axis.set_ylabel("Amplitude")
    axis.set_xlabel("Time [s]")
    plt.title(name)
    if save is True:
        plt.savefig(name+'.png')
    if show is True:
        plt.show()

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
    os.mkdir(dirname_adjusted)
except Exception as e:
    #print(e)
    pass

searchFile(sys.argv[1]) # file search
file_list.sort() # sort (by name)
print(file_list) # show file list

file_check = False
while len(file_list) > 0: # loop until empty list
    wav = file_list[0] # get file name
    (file_dir, file_name) = os.path.split(wav) # path info(dir, name)
    print('file dir:', file_dir)
    print('file_name', file_name)
    data, rate = librosa.load(wav, sr=sample_rate) # open wav file
    
    ''' 
    # if you wanna resampling, try here.
    data, rate = sf.read(wav, dtype='float16')
    data = data.T
    data = librosa.resample(data, sample_rate, 115200)
    '''
    
    data_buf = np.append(data_buf, data) # get data into buffer. data queueing

    if not file_check: # first offset check for shift data
        # + timecheck.
        name_split = file_name.split('_') # ['C', 'OUT', 'ch1', '190809', '163016']
        time_info = datetime(int(name_split[3][0:2]),
                             int(name_split[3][2:4]),
                             int(name_split[3][4:6]),
                             int(name_split[4][0:2]),
                             int(name_split[4][2:4]),
                             int(name_split[4][4:6])) + timedelta(seconds=round(int( offset_size // sample_rate )))
        data_buf = data_buf[offset_size:]
        print("[Notice] shift offset : "+str(offset_size))
        file_check = True

    while len(data_buf) > defined_size:
        print('[Notice] Progressing...')
        sf.write(dirname_adjusted+ '/' +
                 name_split[0] + '_' +
                 name_split[1] + '_' +
                 name_split[2] + '_' +
                 str(time_info)[2:].replace('-','').replace(':','').replace(' ','_') + '.wav',
                 data_buf[:defined_size], sample_rate, subtype='PCM_16')
        time_info = time_info + timedelta(minutes=1)
        data_buf = data_buf[defined_size:] # remove previous data

    del(file_list[0])
    time.sleep(0)

# last file   
if len(data_buf) > 0:
    print('[Notice] lastFile >> Progress')
    sf.write(dirname_adjusted+ '/' +
                 name_split[0] + '_' +
                 name_split[1] + '_' +
                 name_split[2] + '_' +
                 str(time_info)[2:].replace('-','').replace(':','').replace(' ','_') + '.wav',
                 data_buf[:defined_size], sample_rate, subtype='PCM_16')

print('[Notice] Done')