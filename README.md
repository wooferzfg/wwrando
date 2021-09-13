### About

This is a modified version of the randomizer for The Legend of Zelda: The Wind Waker, where all item locations are planned in advance.

**You can download the plandomizer here: https://github.com/wooferzfg/wwrando/releases/latest**

### Plando File Example
```
Permalink: MC4xLjUAd29vZmVycGxhbmRvNQD//z8Cf5DAAwAAQAAAAWsA

Locations:
    Dragon Roost Cavern - Boarded Up Chest: Command Melody
    Dragon Roost Cavern - Chest Across Lava Pit: Grappling Hook
    Dragon Roost Cavern - Dark Room: Power Bracelets
    Dragon Roost Cavern - Pot Room Chest: DRC Small Key
    Dragon Roost Cavern - Mini-Boss: DRC Small Key
    Dragon Roost Cavern - Big Key Chest: Hookshot
    Tower of the Gods - Stone Tablet: Skull Hammer
    Tower of the Gods - Skulls Room Chest: TotG Small Key
    Tower of the Gods - Big Key Chest: TotG Small Key
    Forsaken Fortress - Chest Guarded By Bokoblin: Din's Pearl
    Earth Temple - Transparent Chest In Warp Pot Room: ET Small Key
    Earth Temple - Chest In Three Blocks Room: Progressive Bow
    Earth Temple - Chest Behind Statues: Progressive Bow
    Earth Temple - Stalfos Mini-Boss Room: Triforce Shard 8
    Earth Temple - Many Mirrors Room Right Chest: ET Small Key
    Earth Temple - Many Mirrors Room Left Chest: ET Small Key
    Earth Temple - Jalhalla Heart Container: Earth God's Lyric
    Wind Temple - Chest Between Two Dirt Patches: Hero's Charm
    Wind Temple - Chest Behind Stone Head: WT Small Key
    Wind Temple - Chest at Top of Hub Room: WT Small Key
    Wind Temple - Molgera Heart Container: Wind God's Aria
    Ganon's Tower - Maze Chest: Progressive Bow
    Dragon Roost Island - Chest on Top of Boulder: Iron Boots
    Rock Spire Isle - Cave: Farore's Pearl
    Bird's Peak Rock - Cave: Nayru's Pearl

# Optional - only required when Randomize Starting Island is enabled
Starting Island: Spectacle Island

# Optional - only required when Race Mode is enabled
Race Mode Dungeons:
    - Dragon Roost Cavern
    - Tower of the Gods

# Optional - only required when entrances are randomized
Entrances:
    Dungeon Entrance On Dragon Roost Island: Fire Mountain Secret Cave
    Dungeon Entrance In Forest Haven Sector: Dragon Roost Island Secret Cave
    Dungeon Entrance In Tower of the Gods Sector: Ice Ring Isle Secret Cave
    Dungeon Entrance On Headstone Island: Stone Watcher Island Secret Cave
    Dungeon Entrance On Gale Isle: Tower of the Gods
    Secret Cave Entrance on Outset Island: Cliff Plateau Isles Secret Cave
    Secret Cave Entrance on Dragon Roost Island: Pawprint Isle Chuchu Cave
    Secret Cave Entrance on Fire Mountain: Bomb Island Secret Cave
    Secret Cave Entrance on Ice Ring Isle: Overlook Island Secret Cave
    Secret Cave Entrance on Private Oasis: Bird's Peak Rock Secret Cave
    Secret Cave Entrance on Needle Rock Isle: Star Island Secret Cave
    Secret Cave Entrance on Angular Isles: Diamond Steppe Island Warp Maze Cave
    Secret Cave Entrance on Boating Course: Wind Temple
    Secret Cave Entrance on Stone Watcher Island: Needle Rock Isle Secret Cave
    Secret Cave Entrance on Overlook Island: Earth Temple
    Secret Cave Entrance on Bird's Peak Rock: Horseshoe Island Secret Cave
    Secret Cave Entrance on Pawprint Isle: Angular Isles Secret Cave
    Secret Cave Entrance on Pawprint Isle Side Isle: Pawprint Isle Wizzrobe Cave
    Secret Cave Entrance on Diamond Steppe Island: Rock Spire Isle Secret Cave
    Secret Cave Entrance on Bomb Island: Dragon Roost Cavern
    Secret Cave Entrance on Rock Spire Isle: Cabana Labyrinth
    Secret Cave Entrance on Shark Island: Shark Island Secret Cave
    Secret Cave Entrance on Cliff Plateau Isles: Boating Course Secret Cave
    Secret Cave Entrance on Horseshoe Island: Forbidden Woods
    Secret Cave Entrance on Star Island: Savage Labyrinth
```

### Information

The plandomizer only supports the North American GameCube version of Wind Waker. (MD5: d8e4d45af2032a081a0f446384e9261b)  
The European and Japanese versions of Wind Waker won't work, and neither will Wind Waker HD.

If you're going to play on emulator, you should use the latest development version of Dolphin which can be found at the top of this page: https://dolphin-emu.org/download/  
Note that the GameCube boot up animation in Dolphin doesn't work with the plandomizer and will cause the game to crash before reaching the main menu. If you have previously set Dolphin up to play that animation you will need to disable it before launching the randomized game by going to Config -> GameCube in Dolphin and checking "Skip Main Menu".  

### Running the plandomizer from source

If you want to run the latest development/beta version of the plandomizer from source, follow the instructions below.

Download and install git from here: https://git-scm.com/downloads  
Then clone this repository with git by running this in a command prompt:  
`git clone https://github.com/LagoLunatic/wwrando.git`  

Download and install Python 3.8.2 from here: https://www.python.org/downloads/release/python-382/  
"Windows x86-64 executable installer" is the one you want if you're on Windows, "macOS 64-bit installer" if you're on Mac.  
If you're on Linux, run this command instead: `sudo apt-get install python3.8`  

Open the wwrando folder in a command prompt and install dependencies by running:  
`py -3.8 -m pip install -r requirements.txt` (on Windows)  
`python3 -m pip install -r requirements.txt` (on Mac)  
`python3 -m pip install $(cat requirements.txt) --user` (on Linux)  

Then run the plandomizer with:  
`py -3.8 wwrando.py` (on Windows)  
`python3 wwrando.py` (on Mac)  
`python3 wwrando.py` (on Linux)  

Optionally, you can also install `requirements_full.txt` with the same process you used for `requirements.txt` above.  
`requirements_full.txt` will install additional libraries that speed up texture recoloring, as well as for building a distributable version of the plandomizer. You can still run the plandomizer from source without these.  
