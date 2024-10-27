This project consists of four modes. 
Mode 1-> Volume Adjustment Mode. This mode is activated by the index finger of your left hand.  The modules used were pycaw and numpy. The volume of your system will be adjusted based on the distance between your right thumb and right index finger.
Mdde 2-> Brightness Adjustment Mode. Activated by the in index and middele finger of your left hand. Similar logic to mode 1 but instead of pycaw, screen-brightness-control module was used. 
Mode 3-> Screenshot Mode. Activaed by opening the index, middle and ring finger of the left hand. Pyauotogui and math modules are used here. A screenshot is taken, saved and dispalyed the right index and thumb are in contact
Mode 4-> Recorder Mode. Activated by Activaed by opening the index, middle, ring and pinky finger of the left hand. Pyaudio and vosk modules were used for this. Your speech will be recognized and transcribed to text which will be saved in a txt file called spoke_words.txt


Mediapipe's landhandmarks made these modes possible. In my custom module, you will be able to easily identify, draw and extract the left and right handlandmarks you need. 
