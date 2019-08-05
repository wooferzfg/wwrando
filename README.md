
### About

NO RANDOMIZATION!

This is an ISO patcher for The Legend of Zelda: The Wind Waker based on [wwrando](https://github.com/LagoLunatic/wwrando).
Given the specific use of this program, I used brainfubar's fork of wwrando as a reference since he was going for a similar yet different end result.


The goal is to add features found in wwrando to an otherwise vanilla ISO.

All cosmetic changes are available, but "casual" outfits will only be seen before getting the tunic or during New Game+
Gecko codes can override tunic if desired.

You can toggle the following on/off:
* Swift Sail replaces sail
* Instant Text Boxes
* Faster Block Moving
* Faster Grapple Hook
* Faster Rolling Speed
* Faster Crawling, Climbing, NPC chat zoom
* Tingle Chests Without Tuner
* Invert Camera to match HD
* Reveal Full Sea Chart when making a new file

You can apply the widescreen patch



If you're looking for only skin customization check out brainfubar's release: https://github.com/brainfubar/wwrando

### Download

See the [releases page](https://github.com/WideBoner/wwrando/releases) to download zip files containing the program and assets.
Source works, builds fail to read from ASM path not sure why.

### Information

This program only supports the North American Gamecube version of Wind Waker. (MD5: d8e4d45af2032a081a0f446384e9261b)  
The European and Japanese versions of Wind Waker won't work, and neither will Wind Waker HD.

If you're going to play on emulator, you should use the latest development version of Dolphin which can be found at the top of this page: https://dolphin-emu.org/download/

### Running from source

Download and install git from here: https://git-scm.com/downloads  
Then clone this repository with git by running this in a command prompt:  
`git clone https://github.com/LagoLunatic/wwrando.git`  

Download and install Python 3.6.6 from here: https://www.python.org/downloads/release/python-366/  
"Windows x86-64 executable installer" is the one you want if you're on Windows, "macOS 64-bit installer" if you're on Mac.  

Open the wwrando folder in a command prompt and install dependencies by running:  
`py -3.6 -m pip install -r requirements.txt` (on Windows)  
`python3 -m pip install -r requirements.txt` (on Mac)  

Then run the randomizer with:  
`py -3.6 wwrando.py` (on Windows)  
`python3 wwrando.py` (on Mac)  

In addition, follow this if you want to use PyInstaller to build a distributable version of the randomizer:  
* Install one of PyInstaller's dependencies manually: `py -3.6 -m pip install pywin32-ctypes==0.2.0`  
* Install PyInstaller: `py -3.6 -m pip install PyInstaller==3.4`  
* Then to make a build in the `dist` directory: `build.bat`  

### Discord Server

If you have any questions or are looking for people to play/race with, why not join the official Wind Waker Randomizer Discord server?  
https://discord.gg/r2963mt

### Credits

The randomizer was created and programmed by LagoLunatic, with help from:  
MelonSpeedruns (game design, graphic design)  
Hypatia (textures)  
SageOfMirrors (file format documentation)  
LordNed (file format documentation)  
CryZe (event flag documentation)  
