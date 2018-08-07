
### About

This is a randomizer for The Legend of Zelda: The Wind Waker.  
It randomizes all the items in the game so that each playthrough is unique and you never know where a particular item will be.  
It also makes the game completely open world from the start, removes most cutscenes from the game, and increases sailing speed and text speed.

Download it here: https://github.com/LagoLunatic/wwrando/releases/latest

### Information

The randomizer only supports the North American Gamecube version of Wind Waker. (MD5: d8e4d45af2032a081a0f446384e9261b)  
The European and Japanese versions of Wind Waker won't work, and neither will Wind Waker HD.

The randomizer guarantees that every playthrough will be completable, and that you don't need to use any glitches or tricks to beat it.

All items are randomized, but because Wind Waker is such a large game, a single run of it would take a very long time if you had to check every single location. Therefore the randomizer has options to limit where progress items can appear based on the type of the location.  
For example, you can limit progress items to appearing in dungeons and secret caves only, or secret caves sidequests and mail, or any other combination you want.  
Location types that you don't select will only have unimportant items that you don't need to beat the game - like rupees, heart pieces, quiver upgrades, etc. So you can skip checking them entirely, unless you want some of those optional items.

If you seem to be stuck and can't find anywhere to progress, you should first consult the spoiler log. The spoiler log is generated at the same time as the randomized ISO, and is put in the same folder. It contains information on everything that was randomized in this seed, and lists the order you can get progress items in as well.

If you've consulted the spoiler log and you're still stuck, it's possible you've encountered a bug in the randomizer.  
Please report bugs like that here: https://github.com/LagoLunatic/wwrando/issues  
In the bug report be sure to include the permalink for the seed you encountered the bug on.

If you're going to play on emulator, you should always use the latest development version of Dolphin which can be found at the top of this page: https://dolphin-emu.org/download/  
If you try to run the randomizer on an old version of Dolphin you will most likely get a black screen when booting it up.

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

### Running the randomizer on Mac and Linux

There are currently no official Mac or Linux builds of the randomizer, but you should be able to run the Windows builds with Wine.

For Mac:   
`brew cask install xquartz`  
`brew install wine`  
`sudo wine "Wind Waker Randomizer.exe"`  

For Linux:  
`sudo apt install wine64` or `sudo apt install wine32`  
`wine Wind\ Waker\ Randomizer.exe`  

### Running the randomizer from source

If you want to run the latest development/beta version of the randomizer from source, follow these instructions:  
* Clone this repository in git by running this in a command prompt: `git clone https://github.com/LagoLunatic/wwrando.git`  
* Download and install Python 3.4.4 32-bit from here: https://www.python.org/downloads/release/python-344/ ("Windows x86 MSI installer" is the one you want)  
* Open the wwrando folder in a command prompt and install dependencies by running: `pip install -r requirements.txt`  
* Then run the randomizer with: `python wwrando.py`  
