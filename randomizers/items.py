
import os
import re

from fs_helpers import *
import tweaks

def randomize_items(self):
  print("Randomizing items...")
  
  if not self.options.get("keylunacy"):
    randomize_dungeon_items(self)
  
  randomize_progression_items(self)
  
  # Place unique non-progress items.
  while self.logic.unplaced_nonprogress_items:
    accessible_undone_locations = self.logic.get_accessible_remaining_locations()
    
    item_name = self.rng.choice(self.logic.unplaced_nonprogress_items)
    
    possible_locations = self.logic.filter_locations_valid_for_item(accessible_undone_locations, item_name)
    
    if not possible_locations:
      raise Exception("No valid locations left to place non-progress items!")
    
    location_name = self.rng.choice(possible_locations)
    self.logic.set_location_to_item(location_name, item_name)
  
  accessible_undone_locations = self.logic.get_accessible_remaining_locations()
  inaccessible_locations = [loc for loc in self.logic.remaining_item_locations if loc not in accessible_undone_locations]
  if inaccessible_locations:
    print("Inaccessible locations:")
    for location_name in inaccessible_locations:
      print(location_name)
  
  # Fill remaining unused locations with consumables (Rupees, spoils, and bait).
  locations_to_place_consumables_at = self.logic.remaining_item_locations.copy()
  for location_name in locations_to_place_consumables_at:
    possible_items = self.logic.filter_items_valid_for_location(self.logic.unplaced_consumable_items, location_name)
    item_name = self.rng.choice(possible_items)
    self.logic.set_location_to_item(location_name, item_name)

def randomize_dungeon_items(self):
  # Places dungeon-specific items first so all the dungeon locations don't get used up by other items.
    self.logic.set_prerandomization_dungeon_item_location("Dragon Roost Cavern - First Room", "DRC Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Dragon Roost Cavern - Boarded Up Chest", "DRC Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Dragon Roost Cavern - Rat Room Boarded Up Chest", "DRC Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Dragon Roost Cavern - Bird's Nest", "DRC Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Forbidden Woods - Vine Maze Far Chest", "FW Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Tower of the Gods - Hop Across Floating Boxes", "TotG Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Tower of the Gods - Floating Platforms Room", "TotG Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Earth Temple - Transparent Chest in First Crypt", "ET Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Earth Temple - Casket in Second Crypt", "ET Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Earth Temple - End of Foggy Room With Floormasters", "ET Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Wind Temple - Spike Wall Room - First Chest", "WT Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Wind Temple - Chest Behind Seven Armos", "WT Small Key")
    self.logic.set_prerandomization_dungeon_item_location("Dragon Roost Cavern - Big Key Chest", "DRC Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Forbidden Woods - Big Key Chest", "FW Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Tower of the Gods - Big Key Chest", "TotG Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Earth Temple - Big Key Chest", "ET Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Wind Temple - Big Key Chest", "WT Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Dragon Roost Cavern - Big Key Chest", "DRC Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Forbidden Woods - Big Key Chest", "FW Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Tower of the Gods - Big Key Chest", "TotG Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Earth Temple - Big Key Chest", "ET Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Wind Temple - Big Key Chest", "WT Big Key")
    self.logic.set_prerandomization_dungeon_item_location("Dragon Roost Cavern - Alcove With Water Jugs", "DRC Dungeon Map")
    self.logic.set_prerandomization_dungeon_item_location("Forbidden Woods - First Room", "FW Dungeon Map")
    self.logic.set_prerandomization_dungeon_item_location("Tower of the Gods - Chest Behind Bombable Walls", "TotG Dungeon Map")
    self.logic.set_prerandomization_dungeon_item_location("Forsaken Fortress - Chest Outside Upper Jail Cell", "FF Dungeon Map")
    self.logic.set_prerandomization_dungeon_item_location("Earth Temple - Transparent Chest In Warp Pot Room", "ET Dungeon Map")
    self.logic.set_prerandomization_dungeon_item_location("Wind Temple - Chest In Many Cyclones Room", "WT Dungeon Map")
    self.logic.set_prerandomization_dungeon_item_location("Dragon Roost Cavern - Rat Room", "DRC Compass")
    self.logic.set_prerandomization_dungeon_item_location("Forbidden Woods - Vine Maze Near Chest", "FW Compass")
    self.logic.set_prerandomization_dungeon_item_location("Tower of the Gods - Skulls Room Chest", "TotG Compass")
    self.logic.set_prerandomization_dungeon_item_location("Forsaken Fortress - Chest Guarded By Bokoblin", "FF Compass")
    self.logic.set_prerandomization_dungeon_item_location("Earth Temple - Chest In Three Blocks Room", "ET Compass")
    self.logic.set_prerandomization_dungeon_item_location("Wind Temple - Chest In Middle Of Hub Room", "WT Compass")


def randomize_progression_items(self):
  self.logic.set_location_to_item("Windfall Island - Jail - Tingle - First Gift", "Tingle Tuner")
  self.logic.set_location_to_item("Forsaken Fortress - Helmaroc King Heart Container", "Spoils Bag")
  self.logic.set_location_to_item("Dragon Roost Cavern - Mini-Boss", "Grappling Hook")
  self.logic.set_location_to_item("Fire Mountain - Cave - Chest", "Power Bracelets")
  self.logic.set_location_to_item("Ice Ring Isle - Cave - Chest", "Iron Boots")
  self.logic.set_location_to_item("The Great Sea - Beedle's Shop Ship - Bait Bag", "Bait Bag")
  self.logic.set_location_to_item("Forbidden Woods - Mothula Mini-Boss Room", "Boomerang")
  self.logic.set_location_to_item("Wind Temple - Wizzrobe Mini-Boss Room", "Hookshot")
  self.logic.set_location_to_item("Dragon Roost Island - Chest on Top of Boulder", "Delivery Bag")
  self.logic.set_location_to_item("Windfall Island - Pirate Ship", "Bombs")
  self.logic.set_location_to_item("Forsaken Fortress - Phantom Ganon", "Skull Hammer")
  self.logic.set_location_to_item("Forest Haven - On Tree Branch", "Deku Leaf")
  self.logic.set_location_to_item("Earth Temple - Stalfos Mini-Boss Room", "Mirror Shield")
  
  self.logic.set_location_to_item("Greatfish Isle - Sunken Treasure", "Triforce Shard 1")
  self.logic.set_location_to_item("Gale Isle - Sunken Treasure", "Triforce Shard 2")
  self.logic.set_location_to_item("Stone Watcher Island - Sunken Treasure", "Triforce Shard 3")
  self.logic.set_location_to_item("Outset Island - Sunken Treasure", "Triforce Shard 4")
  self.logic.set_location_to_item("Cliff Plateau Isles - Sunken Treasure", "Triforce Shard 5")
  self.logic.set_location_to_item("Southern Triangle Island - Sunken Treasure", "Triforce Shard 6")
  self.logic.set_location_to_item("Seven-Star Isles - Sunken Treasure", "Triforce Shard 7")
  self.logic.set_location_to_item("Two-Eye Reef - Sunken Treasure", "Triforce Shard 8")
  
  self.logic.set_location_to_item("Islet of Steel - Interior", "Triforce Chart 1")
  self.logic.set_location_to_item("Private Oasis - Cabana Labyrinth - Second Chest", "Triforce Chart 2")
  self.logic.set_location_to_item("Bird's Peak Rock - Cave", "Triforce Chart 3")
  self.logic.set_location_to_item("The Great Sea - Ghost Ship", "Triforce Chart 4")
  self.logic.set_location_to_item("Needle Rock Isle - Golden Gunboat", "Triforce Chart 5")
  self.logic.set_location_to_item("Outset Island - Savage Labyrinth - Floor 30", "Triforce Chart 6")
  self.logic.set_location_to_item("Stone Watcher Island - Cave", "Triforce Chart 7")
  self.logic.set_location_to_item("Overlook Island - Cave", "Triforce Chart 8")
  
  self.logic.set_location_to_item("Greatfish Isle - Hidden Chest", "Nayru's Pearl")
  self.logic.set_location_to_item("Dragon Roost Cavern - Gohma Heart Container", "Din's Pearl")
  self.logic.set_location_to_item("Forbidden Woods - Kalle Demos Heart Container", "Farore's Pearl")
  
  self.logic.set_location_to_item("Tower of the Gods - Stone Tablet", "Command Melody")
  self.logic.set_location_to_item("Dragon Roost Island - Wind Shrine", "Earth God's Lyric")
  self.logic.set_location_to_item("The Great Sea - Cyclos", "Wind God's Aria")
  self.logic.set_location_to_item("Windfall Island - Tott", "Song of Passing")
  
  self.logic.set_location_to_item("Dragon Roost Island - Rito Aerie - Baito", "Note to Mom")
  self.logic.set_location_to_item("Windfall Island - Maggie - Letter", "Maggie's Letter")
  self.logic.set_location_to_item("Windfall Island - Cafe Bar - Postman", "Moblin's Letter")
  self.logic.set_location_to_item("Windfall Island - Mrs. Marie - Give 21 Joy Pendants", "Cabana Deed")
  
  self.logic.set_location_to_item("Two-Eye Reef - Big Octo Great Fairy", "Magic Meter Upgrade")

  self.logic.set_location_to_item("Diamond Steppe Island - Warp Maze Cave - Second Chest", "Ghost Ship Chart")
  
  self.logic.set_location_to_item("Tower of the Gods - Gohdan Heart Container", "Progressive Sword")
  self.logic.set_location_to_item("Earth Temple - Jalhalla Heart Container", "Progressive Sword")
  self.logic.set_location_to_item("Wind Temple - Molgera Heart Container", "Progressive Sword")
  
  self.logic.set_location_to_item("Tower of the Gods - Darknut Mini-Boss Room", "Progressive Bow")
  self.logic.set_location_to_item("Mother and Child Isles - Inside Mother Isle", "Progressive Bow")
  self.logic.set_location_to_item("Ganon's Tower - Maze Chest", "Progressive Bow")
  
  self.logic.set_location_to_item("Northern Fairy Island - Great Fairy", "Progressive Wallet")
  self.logic.set_location_to_item("Outset Island - Great Fairy", "Progressive Wallet")
  
  self.logic.set_location_to_item("Windfall Island - Jail - Maze Chest", "Progressive Picto Box")
  self.logic.set_location_to_item("Windfall Island - Lenzo's House - Bring Forest Firefly", "Progressive Picto Box")
  
  self.logic.set_location_to_item("Windfall Island - Mila", "Empty Bottle")
  self.logic.set_location_to_item("Bomb Island - Submarine", "Empty Bottle")
  self.logic.set_location_to_item("Rock Spire Isle - Beedle's Special Shop Ship - 500 Rupee Item", "Empty Bottle")
  self.logic.set_location_to_item("Rock Spire Isle - Beedle's Special Shop Ship - 950 Rupee Item", "Empty Bottle")
  
  self.logic.set_location_to_item("Outset Island - Underneath Link's House", "Telescope")
  self.logic.set_location_to_item("Windfall Island - Zunari - Stock Exotic Flower in Zunari's Shop", "Magic Armor")
  self.logic.set_location_to_item("Windfall Island - Mrs. Marie - Give 40 Joy Pendants", "Hero's Charm")
  
  self.logic.set_location_to_item("Outset Island - Orca - Give 10 Knight's Crests", "Hurricane Spin")

  self.logic.set_location_to_item("Eastern Fairy Island - Great Fairy", "Progressive Bomb Bag")
  self.logic.set_location_to_item("Southern Fairy Island - Great Fairy", "Progressive Bomb Bag")
  self.logic.set_location_to_item("Western Fairy Island - Great Fairy", "Progressive Quiver")
  self.logic.set_location_to_item("Thorned Fairy Island - Great Fairy", "Progressive Quiver")
  
  self.logic.set_location_to_item("Boating Course - Cave", "Submarine Chart")
  self.logic.set_location_to_item("Mailbox - Letter Advertising Bombs in Beedle's Shop", "Beedle's Chart")
  self.logic.set_location_to_item("Flight Control Platform - Submarine", "Platform Chart")
  self.logic.set_location_to_item("Cyclops Reef - Sunken Treasure", "Light Ring Chart")
  self.logic.set_location_to_item("Overlook Island - Sunken Treasure", "Secret Cave Chart")
  self.logic.set_location_to_item("Four-Eye Reef - Sunken Treasure", "Great Fairy Chart")
  self.logic.set_location_to_item("Northern Triangle Island - Sunken Treasure", "Octo Chart")
  self.logic.set_location_to_item("Windfall Island - Jail - Tingle - Second Gift", "Tingle's Chart")

  # Make sure locations that should have dungeon items in them have them properly placed, even if the above logic missed them for some reason.
  for location_name in self.logic.prerandomization_dungeon_item_locations:
    if location_name in self.logic.remaining_item_locations:
      dungeon_item_name = self.logic.prerandomization_dungeon_item_locations[location_name]
      self.logic.set_location_to_item(location_name, dungeon_item_name)
  
  game_beatable = self.logic.check_requirement_met("Can Reach and Defeat Ganondorf")
  if not game_beatable:
    raise Exception("Game is not beatable on this seed! This error shouldn't happen.")

def write_changed_items(self):
  for location_name, item_name in self.logic.done_item_locations.items():
    paths = self.logic.item_locations[location_name]["Paths"]
    for path in paths:
      change_item(self, path, item_name)

def change_item(self, path, item_name):
  item_id = self.item_name_to_id[item_name]
  
  rel_match = re.search(r"^(rels/[^.]+\.rel)@([0-9A-F]{4})$", path)
  main_dol_match = re.search(r"^main.dol@([0-9A-F]{6})$", path)
  custom_symbol_match = re.search(r"^CustomSymbol:(.+)$", path)
  chest_match = re.search(r"^([^/]+/[^/]+\.arc)(?:/Layer([0-9a-b]))?/Chest([0-9A-F]{3})$", path)
  event_match = re.search(r"^([^/]+/[^/]+\.arc)/Event([0-9A-F]{3}):[^/]+/Actor([0-9A-F]{3})/Action([0-9A-F]{3})$", path)
  scob_match = re.search(r"^([^/]+/[^/]+\.arc)(?:/Layer([0-9a-b]))?/ScalableObject([0-9A-F]{3})$", path)
  actor_match = re.search(r"^([^/]+/[^/]+\.arc)(?:/Layer([0-9a-b]))?/Actor([0-9A-F]{3})$", path)
  
  if rel_match:
    rel_path = rel_match.group(1)
    offset = int(rel_match.group(2), 16)
    path = os.path.join("files", rel_path)
    change_hardcoded_item(self, path, offset, item_id)
  elif main_dol_match:
    offset = int(main_dol_match.group(1), 16)
    path = os.path.join("sys", "main.dol")
    change_hardcoded_item(self, path, offset, item_id)
  elif custom_symbol_match:
    custom_symbol = custom_symbol_match.group(1)
    if custom_symbol not in self.custom_symbols:
      raise Exception("Invalid custom symbol: %s" % custom_symbol)
    address = self.custom_symbols[custom_symbol]
    offset = address - tweaks.ORIGINAL_FREE_SPACE_RAM_ADDRESS + tweaks.ORIGINAL_DOL_SIZE
    path = os.path.join("sys", "main.dol")
    change_hardcoded_item(self, path, offset, item_id)
  elif chest_match:
    arc_path = "files/res/Stage/" + chest_match.group(1)
    if chest_match.group(2):
      layer = int(chest_match.group(2), 16)
    else:
      layer = None
    chest_index = int(chest_match.group(3), 16)
    change_chest_item(self, arc_path, chest_index, layer, item_id)
  elif event_match:
    arc_path = "files/res/Stage/" + event_match.group(1)
    event_index = int(event_match.group(2), 16)
    actor_index = int(event_match.group(3), 16)
    action_index = int(event_match.group(4), 16)
    change_event_item(self, arc_path, event_index, actor_index, action_index, item_id)
  elif scob_match:
    arc_path = "files/res/Stage/" + scob_match.group(1)
    if scob_match.group(2):
      layer = int(scob_match.group(2), 16)
    else:
      layer = None
    scob_index = int(scob_match.group(3), 16)
    change_scob_item(self, arc_path, scob_index, layer, item_id)
  elif actor_match:
    arc_path = "files/res/Stage/" + actor_match.group(1)
    if actor_match.group(2):
      layer = int(actor_match.group(2), 16)
    else:
      layer = None
    actor_index = int(actor_match.group(3), 16)
    change_actor_item(self, arc_path, actor_index, layer, item_id)
  else:
    raise Exception("Invalid item path: " + path)

def change_hardcoded_item(self, path, offset, item_id):
  data = self.get_raw_file(path)
  write_u8(data, offset, item_id)

def change_chest_item(self, arc_path, chest_index, layer, item_id):
  if arc_path.endswith("Stage.arc"):
    dzx = self.get_arc(arc_path).get_file("stage.dzs")
  else:
    dzx = self.get_arc(arc_path).get_file("room.dzr")
  chest = dzx.entries_by_type_and_layer("TRES", layer)[chest_index]
  chest.item_id = item_id
  chest.save_changes()

def change_event_item(self, arc_path, event_index, actor_index, action_index, item_id):
  event_list = self.get_arc(arc_path).get_file("event_list.dat")
  action = event_list.events[event_index].actors[actor_index].actions[action_index]
  
  if 0x6D <= item_id <= 0x72: # Song
    action.name = "059get_dance"
    action.properties[0].value = [item_id-0x6D]
  else:
    action.name = "011get_item"
    action.properties[0].value = [item_id]

def change_scob_item(self, arc_path, scob_index, layer, item_id):
  if arc_path.endswith("Stage.arc"):
    dzx = self.get_arc(arc_path).get_file("stage.dzs")
  else:
    dzx = self.get_arc(arc_path).get_file("room.dzr")
  scob = dzx.entries_by_type_and_layer("SCOB", layer)[scob_index]
  if scob.is_salvage():
    scob.salvage_item_id = item_id
    scob.save_changes()
  elif scob.is_buried_pig_item():
    scob.buried_pig_item_id = item_id
    scob.save_changes()
  else:
    raise Exception("%s/SCOB%03X is an unknown type of SCOB" % (arc_path, scob_index))

def change_actor_item(self, arc_path, actor_index, layer, item_id):
  if arc_path.endswith("Stage.arc"):
    dzx = self.get_arc(arc_path).get_file("stage.dzs")
  else:
    dzx = self.get_arc(arc_path).get_file("room.dzr")
  actr = dzx.entries_by_type_and_layer("ACTR", layer)[actor_index]
  if actr.is_item():
    actr.item_id = item_id
  elif actr.is_boss_item():
    actr.boss_item_id = item_id
  else:
    raise Exception("%s/ACTR%03X is not an item" % (arc_path, actor_index))
  
  actr.save_changes()
