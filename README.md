# Dependencies
```bash
sudo apt-get install python3 python3-dev python3-setuptools python3-pip
pip install numpy librosa
```

# wave-shifting
1. Put `*.wav` files into ${TARGET_DIR} directory  
2. `python wave_shift.py ${TARGET_DIR} ${SAMPLE_RATE} ${SHIFT_OFFSET}  

- ${TARGET_DIR} : Target directory name  
- ${SAMPLE_RATE} : 48000, 96000, ... , 192000, etc..  
- ${SHIFT_OFFSET} : seconds * ${SAMPLE_RATE}  

> give offset. (2 seconds)  
> python wave_shift.py TEST 192000 384000  

3. Check ${TARGET_DIR}+`_modified` directory

# check-overrun
1. Put `*.wav` files into ${TARGETR_DIR} directory
2. `python check_overrun.py ${TARGET_DIR} ${LENGTH}

- ${TARGET_DIR} : Target directory name  
- ${LENGTH} : for checking overrun size  

> give length. (0.001 sec)  
> python check_overrun.py ${TARGET_DIR} ${LENGTH}  

3. Chech ${TARGET_DIR}+`_overrun` directory  