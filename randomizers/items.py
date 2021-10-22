
import os
import re
from collections import OrderedDict

from fs_helpers import *
import tweaks

def randomize_items(self):
  print("Randomizing items...")

  # If the plando placed items in every location, then we skip all this
  if not self.logic.remaining_item_locations or not self.logic.unplaced_progress_items:
    return

  if self.options.get("race_mode"):
    self.race_mode_required_dungeons = self.plando["Race Mode Dungeons"]

  if not self.logic.remaining_item_locations or not self.logic.unplaced_nonprogress_items:
    return
  
  accessible_undone_locations = self.logic.remaining_item_locations
  inaccessible_locations = [loc for loc in self.logic.remaining_item_locations if loc not in accessible_undone_locations]
  if inaccessible_locations:
    print("Inaccessible locations:")
    for location_name in inaccessible_locations:
      print(location_name)
  
  if not self.logic.remaining_item_locations or not self.logic.unplaced_fixed_consumable_items:
    return

  # Fill remaining unused locations with consumables (Rupees, spoils, and bait).
  locations_to_place_consumables_at = self.logic.remaining_item_locations.copy()
  for location_name in locations_to_place_consumables_at:
    possible_items = self.logic.filter_items_valid_for_location(self.logic.unplaced_fixed_consumable_items, location_name)
    if len(possible_items) == 0:
      possible_items = self.logic.filter_items_valid_for_location(self.logic.duplicatable_consumable_items, location_name)
      if len(possible_items) == 0:
        raise Exception("No valid consumable items for location %s" % location_name)
    
    item_name = self.rng.choice(possible_items)
    self.logic.set_location_to_item(location_name, item_name)

def write_changed_items(self):
  for location_name, item_name in self.logic.done_item_locations.items():
    paths = self.logic.item_locations[location_name]["Paths"]
    for path in paths:
      change_item(self, path, item_name)

def change_item(self, path, item_name):
  item_id = self.item_name_to_id[item_name]
  
  rel_match = re.search(r"^(rels/[^.]+\.rel)@([0-9A-F]{4})$", path)
  main_dol_match = re.search(r"^main.dol@(8[0-9A-F]{7})$", path)
  custom_symbol_match = re.search(r"^CustomSymbol:(.+)$", path)
  chest_match = re.search(r"^([^/]+/[^/]+\.arc)(?:/Layer([0-9a-b]))?/Chest([0-9A-F]{3})$", path)
  event_match = re.search(r"^([^/]+/[^/]+\.arc)/Event([0-9A-F]{3}):[^/]+/Actor([0-9A-F]{3})/Action([0-9A-F]{3})$", path)
  scob_match = re.search(r"^([^/]+/[^/]+\.arc)(?:/Layer([0-9a-b]))?/ScalableObject([0-9A-F]{3})$", path)
  actor_match = re.search(r"^([^/]+/[^/]+\.arc)(?:/Layer([0-9a-b]))?/Actor([0-9A-F]{3})$", path)
  
  if rel_match:
    rel_path = rel_match.group(1)
    offset = int(rel_match.group(2), 16)
    path = os.path.join("files", rel_path)
    change_hardcoded_item_in_rel(self, path, offset, item_id)
  elif main_dol_match:
    address = int(main_dol_match.group(1), 16)
    change_hardcoded_item_in_dol(self, address, item_id)
  elif custom_symbol_match:
    custom_symbol = custom_symbol_match.group(1)
    if custom_symbol not in self.main_custom_symbols:
      raise Exception("Invalid custom symbol: %s" % custom_symbol)
    address = self.main_custom_symbols[custom_symbol]
    change_hardcoded_item_in_dol(self, address, item_id)
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

def change_hardcoded_item_in_dol(self, address, item_id):
  self.dol.write_data(write_u8, address, item_id)

def change_hardcoded_item_in_rel(self, path, offset, item_id):
  rel = self.get_rel(path)
  rel.write_data(write_u8, offset, item_id)

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
  if scob.actor_class_name in ["d_a_salvage", "d_a_tag_kb_item"]:
    scob.item_id = item_id
    scob.save_changes()
  else:
    raise Exception("%s/SCOB%03X is an unknown type of SCOB" % (arc_path, scob_index))

def change_actor_item(self, arc_path, actor_index, layer, item_id):
  if arc_path.endswith("Stage.arc"):
    dzx = self.get_arc(arc_path).get_file("stage.dzs")
  else:
    dzx = self.get_arc(arc_path).get_file("room.dzr")
  actr = dzx.entries_by_type_and_layer("ACTR", layer)[actor_index]
  if actr.actor_class_name in ["d_a_item", "d_a_boss_item"]:
    actr.item_id = item_id
  else:
    raise Exception("%s/ACTR%03X is not an item" % (arc_path, actor_index))
  
  actr.save_changes()
