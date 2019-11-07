
### About

Better Wind Waker  

This is an ISO patcher for The Legend of Zelda: The Wind Waker based on [LagoLunatic's wwrando](https://github.com/LagoLunatic/wwrando), and [brainfubar's fork](https://github.com/brainfubar/wwrando).  

**This adds features from the Wind Waker Randomizer to an ISO without randomization.**  
Intended to make a more enjoyable casual experience reflecting many changes made for Wind Waker HD.  

You can toggle the following on/off:
* Swift Sail replaces Sail  
* Instant text boxes  
* Faster block moving  
* Faster grapple hook  
* Faster rolling speed  
* Faster crawling, climbing, NPC chat zoom  
* Tingle chests without tuner 
* Turn while swinging or grappling
* Reveal full sea chart 
* Free-roam boat  
* No song replays  
* Invert camera  
* Remove intro video  
* Faster ballad of gales  
 

  
**Custom Player Models**  

Allows you to customize Link, but "casual" outfits will only be seen before getting the tunic or during New Game+  
  
Models can be found here:  
https://github.com/Sage-of-Mirrors/Custom-Wind-Waker-Player-Models  
https://gamebanana.com/games/6173  
https://discord.gg/r2963mt (WIP models, learn to make your own)  

### Download

Beta release available now, no issues are known. (64-bit only right now)

https://github.com/WideBoner/betterww/releases

### Other Tweaks
  
You can apply the [Widescreen Patch](https://www.dropbox.com/s/5huyf6r3drynq1c/The%20Legend%20of%20Zelda%20The%20Wind%20Waker%20Widescreen.zip?dl=1)  

You can apply the [Female Pronoun Patch](http://slothsoft.tumblr.com/post/36097890951/the-legend-of-zelda-the-wind-waker-pronoun)  

If using Dolphin you can use [Hypatia's HD Texture Pack](https://onthegreatsea.tumblr.com/DOWNLOADS)

Gecko codes you may want to use:  

  
Second set of equipped items:  
283ED84A FFFB0004  
A8000000 00000000  
C0000000 0000000B  
3D80803C 618CA7DB  
892C0000 A14C0001  
80A62EA8 2C050000  
4082001C 99262EA1  
B1462EA2 89262EA5  
A1462EA6 38A00001  
48000018 99262EA5  
B1462EA6 89262EA1  
A1462EA2 38A00000  
992C0000 B14C0001  
90A62EA8 4E800020  
04205734 60000000  
E0000000 80008000  
(D-pad down to switch)  
  
Hero Mode:  
040C7D4C 60000000  
C21F169C 00000003  
8061000C 74648000  
41820008 1C630002  
60000000 00000000  
(Take double damage, no heart drops)  
  
Items don't disappear:  
040F6E38 38600000  
  
Unrestricted Camera:  
04356D34 45000000  
04356D48 42B00000  
  
Blur off:  
043FCB9C 00000000  


### Information

This program only supports the North American Gamecube version of Wind Waker. (MD5: d8e4d45af2032a081a0f446384e9261b)  

This works on Gamecube/Wii/Dolphin.

If you're going to play on emulator, you should use the latest development version of Dolphin which can be found at the top of this page: https://dolphin-emu.org/download/


### Credits

wwrando:  
The randomizer was created and programmed by LagoLunatic, with help from:  
MelonSpeedruns (game design, graphic design)  
Hypatia (textures)  
SageOfMirrors (file format documentation)  
LordNed (file format documentation)  
CryZe (event flag documentation)  

betterww:  
brainfubar (His [fork](https://github.com/brainfubar/wwrando) of wwrando was used to make this)  
MelonSpeedrun (Original design for Brisk Sail)
JarheadHME (help getting releases working and updating)
