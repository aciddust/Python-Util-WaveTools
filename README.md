# Dependencies
```bash
sudo apt-get install python3 python3-dev python3-setuptools python3-pip
pip install numpy librosa
```

# Example
1. Put `*.wav` files into `TEST` directory  
2. `python wave_shift.py ${TARGET_DIR} ${SAMPLE_RATE} ${SHIFT_OFFSET}  

- ${TARGET_DIR} : Target directory name  
- ${SAMPLE_RATE} : 48000, 96000, ... , 192000, etc..  
- ${SHIFT_OFFSET} : seconds * ${SAMPLE_RATE}  

> give 2 seconds offset.  
> python wave_shift.py TEST 192000 384000  

3. Check `TEST_modified` directory
