
from collections import OrderedDict

OPTIONS = OrderedDict([
  (
    "progression_dungeons",
    "This controls whether dungeons can contain progress items.<br><u>If this is not checked, dungeons will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_great_fairies",
    "This controls whether the items given by Great Fairies can be progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_puzzle_secret_caves",
    "This controls whether puzzle-focused secret caves can contain progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_combat_secret_caves",
    "This controls whether combat-focused secret caves can contain progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_short_sidequests",
    "This controls whether sidequests that can be completed quickly can reward progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only reward optional items you don't need to beat the game."
  ),
  (
    "progression_long_sidequests",
    "This controls whether long sidequests (e.g. Lenzo's assistant, withered trees, goron trading) can reward progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only reward optional items you don't need to beat the game."
  ),
  (
    "progression_spoils_trading",
    "This controls whether the items you get by trading in spoils to NPCs can be progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only reward optional items you don't need to beat the game."
  ),
  (
    "progression_minigames",
    "This controls whether minigames can reward progress items (sinking ships, auctions, mail sorting, barrel shooting, bird-man contest).<br><u>If this is not checked, minigames will still be randomized</u>, but will only reward optional items you don't need to beat the game."
  ),
  (
    "progression_free_gifts",
    "This controls whether gifts freely given by NPCs can be progress items (Tott, Salvage Corp, imprisoned Tingle).<br><u>If this is not checked, they will still be randomized</u>, but will only be optional items you don't need to beat the game."
  ),
  (
    "progression_mail",
    "This controls whether mail can contain progress items.<br><u>If this is not checked, mail will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_platforms_rafts",
    "This controls whether lookout platforms and rafts can contain progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_submarines",
    "This controls whether submarines can contain progress items.<br><u>If this is not checked, submarines will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_eye_reef_chests",
    "This controls whether the chests that appear after clearing out the eye reefs can contain progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_big_octos_gunboats",
    "This controls whether the items dropped by Big Octos and Gunboats can contain progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_triforce_charts",
    "This controls whether the sunken treasure chests marked on Triforce Charts can contain progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_treasure_charts",
    "This controls whether the sunken treasure chests marked on Treasure Charts can contain progress items.<br><u>If this is not checked, they will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  (
    "progression_expensive_purchases",
    "This controls whether items that cost a lot of rupees can be progress items (Rock Spire shop, auctions, Tingle's letter, trading quest).<br><u>If this is not checked, they will still be randomized</u>, but will only be optional items you don't need to beat the game."
  ),
  (
    "progression_misc",
    "Miscellaneous locations that don't fit into any of the above categories (outdoors chests, pig, wind shrine, Cyclos etc).<br><u>If this is not checked, they will still be randomized</u>, but will only contain optional items you don't need to beat the game."
  ),
  
  
  (
    "keylunacy",
    "Allows dungeon keys (as well as maps and compasses) to appear anywhere in the game, not just in the dungeon they're for."
  ),
  (
    "randomize_dungeon_entrances",
    "Shuffles around which dungeon entrances take you into which dungeons. (No effect on Forsaken Fortress or Ganon's Tower.)"
  ),
  (
    "randomize_charts",
    "Randomizes which sector is drawn on each Triforce/Treasure Chart."
  ),
  (
    "randomize_starting_island",
    "Randomizes which island you start the game on."
  ),
  
  (
    "swift_sail",
    "Sailing speed is doubled and the direction of the wind is always at your back as long as the sail is out."
  ),
  (
    "instant_text_boxes",
    "Text appears instantly.<br>Also, the B button is changed to instantly skip through text as long as you hold it down."
  ),
  (
    "reveal_full_sea_chart",
    "Start the game with the sea chart fully drawn out."
  ),
  (
    "num_starting_triforce_shards",
    "Change the number of Triforce Shards you start the game with.<br>The higher you set this, the fewer you will need to find placed randomly."
  ),
  (
    "add_shortcut_warps_between_dungeons",
    "Adds new warp pots that act as shortcuts connecting dungeons to each other directly. (DRC, FW, TotG, and separately FF, ET, WT.)\nEach pot must be unlocked before it can be used, so you cannot use them to access dungeons you wouldn't already have access to."
  ),
  (
    "generate_spoiler_log",
    "Generate a text file that lists the location of every single item for this seed.\nNote that whether this is checked or not affects where items are placed in this seed."
  ),
  (
    "sword_mode",
    "Controls whether you start with the Hero's Sword, the Hero's Sword is randomized, or if there are no swords in the entire game."
  ),
  (
    "skip_rematch_bosses",
    "Removes the door in Ganon's Tower that only unlocks when you defeat the rematch versions of Gohma, Kalle Demos, Jalhalla, and Molgera."
  ),
  
  (
    "custom_player_model",
    "Replaces Link's model with a custom player model.\nThese are loaded from the /models folder."
  ),
  (
    "player_in_casual_clothes",
    "Enable this if you want to wear your casual clothes instead of the Hero's Clothes."
  ),
])

NON_PERMALINK_OPTIONS = [
  "custom_player_model",
  "player_in_casual_clothes",
]
