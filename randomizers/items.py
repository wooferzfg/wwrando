
import os
import re

from logic.logic import Logic

from gclib import fs_helpers as fs
from randomizers.base_randomizer import BaseRandomizer
from wwlib.dzx import DZx, ACTR, SCOB, TRES, DZxLayer
from wwlib.events import EventList
from tweaks import add_trap_chest_event_to_stage

class ItemRandomizer(BaseRandomizer):
  def __init__(self, rando):
    super().__init__(rando)
    
    self.item_locations_plando = self.rando.plando.get("Locations")
  
  def is_enabled(self) -> bool:
    return bool(self.rando.randomize_items)
  
  @property
  def progress_randomize_duration_weight(self) -> int:
    return 400
  
  @property
  def progress_save_duration_weight(self) -> int:
    return 100
  
  @property
  def progress_randomize_text(self) -> str:
    return "Randomizing items..."
  
  @property
  def progress_save_text(self) -> str:
    return "Saving items..."
  
  def _randomize(self):
    errors = []
    for location_name, item_name in self.item_locations_plando.items():
      location_name = location_name.strip()
      clean_item_name = self.logic.clean_item_name(item_name)

      if location_name not in self.logic.item_locations:
        errors.append("Location not found: " + location_name)
        continue
      if clean_item_name not in self.logic.all_cleaned_item_names:
        errors.append("Item not found: " + item_name)
        continue

      self.logic.set_location_to_item(location_name, clean_item_name)

    if errors:
      raise Exception("\n".join(errors))
    
    self.randomize_consumable_items()
  
  def _save(self):
    for location_name, item_name in self.logic.done_item_locations.items():
      paths = self.logic.item_locations[location_name]["Paths"]
      for path in paths:
        self.change_item(path, item_name)
  
  def write_to_non_spoiler_log(self) -> str:
    log_str = ""
    
    progress_locations, nonprogress_locations = self.logic.get_progress_and_non_progress_locations()
    
    log_str += "### Locations that may or may not have progress items in them on this run:\n"
    log_str += self.write_list_of_location_names_to_log(progress_locations)
    log_str += "\n\n"
    
    log_str += "### Locations that cannot have progress items in them on this run:\n"
    log_str += self.write_list_of_location_names_to_log(nonprogress_locations)
    
    return log_str
  
  def write_to_spoiler_log(self) -> str:
    spoiler_log = ""
    
    spoiler_log += self.write_progression_spheres_to_log()
    
    spoiler_log += self.write_item_location_spoilers_to_log()
    
    return spoiler_log
  
  
  #region Randomization
  def randomize_consumable_items(self):
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
  #endregion
  
  
  #region Saving
  def change_item(self, path, item_name):
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
      self.change_hardcoded_item_in_rel(path, offset, item_name)
    elif main_dol_match:
      address = int(main_dol_match.group(1), 16)
      self.change_hardcoded_item_in_dol(address, item_name)
    elif custom_symbol_match:
      custom_symbol = custom_symbol_match.group(1)
      found_custom_symbol = False
      for file_path, custom_symbols_for_file in self.rando.custom_symbols.items():
        if custom_symbol in custom_symbols_for_file:
          found_custom_symbol = True
          if file_path == "sys/main.dol":
            address = custom_symbols_for_file[custom_symbol]
            self.change_hardcoded_item_in_dol(address, item_name)
          else:
            offset = custom_symbols_for_file[custom_symbol]
            self.change_hardcoded_item_in_rel(file_path, offset, item_name)
          break
      if not found_custom_symbol:
        raise Exception("Invalid custom symbol: %s" % custom_symbol)
    elif chest_match:
      arc_path = "files/res/Stage/" + chest_match.group(1)
      layer = DZxLayer(chest_match.group(2))
      chest_index = int(chest_match.group(3), 16)
      self.change_chest_item(arc_path, chest_index, layer, item_name)
    elif event_match:
      arc_path = "files/res/Stage/" + event_match.group(1)
      event_index = int(event_match.group(2), 16)
      actor_index = int(event_match.group(3), 16)
      action_index = int(event_match.group(4), 16)
      self.change_event_item(arc_path, event_index, actor_index, action_index, item_name)
    elif scob_match:
      arc_path = "files/res/Stage/" + scob_match.group(1)
      layer = DZxLayer(scob_match.group(2))
      scob_index = int(scob_match.group(3), 16)
      self.change_scob_item(arc_path, scob_index, layer, item_name)
    elif actor_match:
      arc_path = "files/res/Stage/" + actor_match.group(1)
      layer = DZxLayer(actor_match.group(2))
      actor_index = int(actor_match.group(3), 16)
      self.change_actor_item(arc_path, actor_index, layer, item_name)
    else:
      raise Exception("Invalid item path: " + path)

  def change_hardcoded_item_in_dol(self, address, item_name: str):
    item_id = self.rando.item_name_to_id[item_name]
    self.rando.dol.write_data(fs.write_u8, address, item_id)

  def change_hardcoded_item_in_rel(self, path, offset, item_name: str):
    item_id = self.rando.item_name_to_id[item_name]
    rel = self.rando.get_rel(path)
    rel.write_data(fs.write_u8, offset, item_id)

  def change_chest_item(self, arc_path: str, chest_index: int, layer: DZxLayer, item_name: str):
    if arc_path.endswith("Stage.arc"):
      dzx = self.rando.get_arc(arc_path).get_file("stage.dzs", DZx)
    else:
      dzx = self.rando.get_arc(arc_path).get_file("room.dzr", DZx)
    
    chest = dzx.entries_by_type_and_layer(TRES, layer=layer)[chest_index]
    
    if item_name.endswith(" Trap Chest"):
      # The vanilla game stores the chest behavior type in a bitfield
      # with a mask of 0x7F. However, the devs only used the values 0x00 to 0x08.
      # So, in the custom chest code, the behavior type has been reduced to a mask
      # of 0x3F, leaving a single bit with a mask of 0x40 to serve as a flag
      # indicating whether the chest is trapped (set) or normal (unset).
      
      # Here, we set that custom trap flag.
      chest.behavior_type |= 0x40

      stage_name = arc_path.split("/")[-2]
      add_trap_chest_event_to_stage(self.rando, stage_name)
    else:
      item_id = self.rando.item_name_to_id[item_name]
      chest.item_id = item_id
    
    if self.options.chest_type_matches_contents:
      chest.chest_type = self.get_ctmc_chest_type_for_item(item_name)
    
    chest.save_changes()

  def get_ctmc_chest_type_for_item(self, item_name: str):
    if item_name not in self.logic.all_progress_items:
      return 0 # Light wood chests for non-progress items and consumables
    if not item_name.endswith(" Key"):
      return 2 # Metal chests for progress items
    if not self.options.required_bosses:
      return 1 # Dark wood chest for Small and Big Keys
    
    # In required bosses mode, only put the dungeon keys for required dungeons in dark wood chests.
    # The other keys go into light wood chests.
    dungeon_short_name = item_name.split()[0]
    if self.logic.DUNGEON_NAMES[dungeon_short_name] in self.rando.boss_reqs.required_dungeons:
      return 1
    else:
      return 0

  def change_event_item(self, arc_path: str, event_index: int, actor_index: int, action_index: int, item_name: str):
    item_id = self.rando.item_name_to_id[item_name]
    
    event_list = self.rando.get_arc(arc_path).get_file("event_list.dat", EventList)
    action = event_list.events[event_index].actors[actor_index].actions[action_index]
    
    if 0x6D <= item_id <= 0x72: # Song
      action.name = "059get_dance"
      action.properties[0].value = [item_id-0x6D]
    else:
      action.name = "011get_item"
      action.properties[0].value = [item_id]

  def change_scob_item(self, arc_path: str, scob_index: int, layer: DZxLayer, item_name: str):
    item_id = self.rando.item_name_to_id[item_name]
    
    if arc_path.endswith("Stage.arc"):
      dzx = self.rando.get_arc(arc_path).get_file("stage.dzs", DZx)
    else:
      dzx = self.rando.get_arc(arc_path).get_file("room.dzr", DZx)
    
    scob = dzx.entries_by_type_and_layer(SCOB, layer=layer)[scob_index]
    if scob.actor_class_name in ["d_a_salvage", "d_a_tag_kb_item"]:
      scob.item_id = item_id
      scob.save_changes()
    else:
      raise Exception("%s/SCOB%03X is an unknown type of SCOB" % (arc_path, scob_index))

  def change_actor_item(self, arc_path: str, actor_index: int, layer: DZxLayer, item_name: str):
    item_id = self.rando.item_name_to_id[item_name]
    
    if arc_path.endswith("Stage.arc"):
      dzx = self.rando.get_arc(arc_path).get_file("stage.dzs", DZx)
    else:
      dzx = self.rando.get_arc(arc_path).get_file("room.dzr", DZx)
    
    actr = dzx.entries_by_type_and_layer(ACTR, layer=layer)[actor_index]
    if actr.actor_class_name in ["d_a_item", "d_a_boss_item"]:
      actr.item_id = item_id
      if actr.actor_class_name == "d_a_item" and actr.behavior_type == 0:
        # Change field items with the fade out behavior type to have the don't fade out type instead.
        # This affects the "Earth Temple - Casket in Second Crypt" item (though that one would only
        # fade out after opening the casket and reloading the room).
        actr.behavior_type = 3
    elif actr.actor_class_name in ["d_a_tsubo", "d_a_obj_homen"]:
      if item_id == 0x00:
        # Special case - our custom item_id param for these classes uses 0x00 to mean null, so use the vanilla param.
        actr.dropped_item_id = item_id
        actr.item_id = 0x00
      else:
        actr.dropped_item_id = 0x3F
        actr.item_id = item_id
    else:
      raise Exception("%s/ACTR%03X is not an item" % (arc_path, actor_index))
    
    actr.save_changes()
  #endregion
  
  
  #region Logs
  def get_zones_and_max_location_name_len(self, locations):
    zones = {}
    max_location_name_length = 0
    for location_name in locations:
      zone_name, specific_location_name = self.logic.split_location_name_by_zone(location_name)
      
      if zone_name not in zones:
        zones[zone_name] = []
      zones[zone_name].append((location_name, specific_location_name))
      
      if len(specific_location_name) > max_location_name_length:
        max_location_name_length = len(specific_location_name)
    
    return (zones, max_location_name_length)
  
  def write_list_of_location_names_to_log(self, locations) -> str:
    log_str = ""
    
    zones, _ = self.get_zones_and_max_location_name_len(locations)
    format_string = "    %s\n"
    
    for zone_name, locations_in_zone in zones.items():
      if not any(loc for (loc, _) in locations_in_zone if loc in locations):
        # No locations for this zone.
        continue
      
      log_str += zone_name + ":\n"
      
      for (location_name, specific_location_name) in locations_in_zone:
        if location_name in locations:
          log_str += format_string % specific_location_name
    
    return log_str
  
  def write_progression_spheres_to_log(self):
    spoiler_log = "Playthrough progression spheres:\n"
    progression_spheres = self.calculate_playthrough_progression_spheres()
    all_progression_sphere_locations = [loc for locs in progression_spheres for loc in locs]
    zones, max_location_name_length = self.get_zones_and_max_location_name_len(all_progression_sphere_locations)
    format_string = "      %-" + str(max_location_name_length+1) + "s %s\n"
    for i, progression_sphere in enumerate(progression_spheres):
      spoiler_log += "%d:\n" % (i+1)
      
      for zone_name, locations_in_zone in zones.items():
        if not any(loc for (loc, _) in locations_in_zone if loc in progression_sphere):
          # No locations in this zone are used in this sphere.
          continue
        
        spoiler_log += "  %s:\n" % zone_name
        
        for (location_name, specific_location_name) in locations_in_zone:
          if location_name in progression_sphere:
            item_name = progression_sphere[location_name]
            spoiler_log += format_string % (specific_location_name + ":", item_name)
      
    spoiler_log += "\n\n\n"
    return spoiler_log
  
  def write_item_location_spoilers_to_log(self):
    spoiler_log = "All item locations:\n"
    zones, max_location_name_length = self.get_zones_and_max_location_name_len(self.logic.done_item_locations)
    format_string = "    %-" + str(max_location_name_length+1) + "s %s\n"
    for zone_name, locations_in_zone in zones.items():
      spoiler_log += zone_name + ":\n"
      
      for (location_name, specific_location_name) in locations_in_zone:
        item_name = self.logic.done_item_locations[location_name]
        spoiler_log += format_string % (specific_location_name + ":", item_name)
    
    spoiler_log += "\n\n\n"
    return spoiler_log
  #endregion
  
  
  def calculate_playthrough_progression_spheres(self):
    progression_spheres = []
    
    logic = Logic(self.rando)
    previously_accessible_locations = []
    game_beatable = False
    while logic.unplaced_progress_items:
      progress_items_in_this_sphere = {}
      
      accessible_locations = logic.get_accessible_remaining_locations(for_progression=False)
      locations_in_this_sphere = [
        loc for loc in accessible_locations
        if loc not in previously_accessible_locations
      ]
      if not locations_in_this_sphere:
        break
      
      
      if not self.options.keylunacy:
        # If the player gained access to any small keys, we need to give them the keys without counting that as a new sphere.
        newly_accessible_predetermined_item_locations = [
          loc for loc in locations_in_this_sphere
          if loc in self.logic.prerandomization_item_locations
        ]
        newly_accessible_small_key_locations = [
          loc for loc in newly_accessible_predetermined_item_locations
          if self.logic.prerandomization_item_locations[loc].endswith(" Small Key")
        ]
        if newly_accessible_small_key_locations:
          for small_key_location_name in newly_accessible_small_key_locations:
            item_name = self.logic.prerandomization_item_locations[small_key_location_name]
            assert item_name.endswith(" Small Key")
            
            logic.add_owned_item(item_name)
          
          previously_accessible_locations += newly_accessible_small_key_locations
          continue # Redo this loop iteration with the small key locations no longer being considered 'remaining'.
      
      
      # Hide duplicated progression items (e.g. Empty Bottles) when they are placed in non-progression locations to avoid confusion and inconsistency.
      locations_in_this_sphere = logic.filter_locations_for_progression(locations_in_this_sphere)
      
      for location_name in locations_in_this_sphere:
        zone_name, specific_location_name = self.logic.split_location_name_by_zone(location_name)
        if specific_location_name.endswith(" Heart Container"):
          boss_name = specific_location_name.removesuffix(" Heart Container")
          progress_items_in_this_sphere[f"{zone_name} - Boss"] = f"Defeat {boss_name}"
        
        item_name = self.logic.done_item_locations[location_name]
        if item_name in logic.all_progress_items:
          progress_items_in_this_sphere[location_name] = item_name
      
      if not game_beatable:
        game_beatable = logic.check_requirement_met("Can Reach and Defeat Ganondorf")
        if game_beatable:
          progress_items_in_this_sphere["Ganon's Tower - Rooftop"] = "Defeat Ganondorf"
      
      progression_spheres.append(progress_items_in_this_sphere)
      
      for location_name, item_name in progress_items_in_this_sphere.items():
        if item_name.startswith("Defeat "):
          continue
        logic.add_owned_item(item_name)
      for group_name, item_names in logic.progress_item_groups.items():
        entire_group_is_owned = all(item_name in logic.currently_owned_items for item_name in item_names)
        if entire_group_is_owned and group_name in logic.unplaced_progress_items:
          logic.unplaced_progress_items.remove(group_name)
      
      previously_accessible_locations = accessible_locations
    
    if not game_beatable:
      # If the game wasn't already beatable on a previous progression sphere but it is now we add one final one just for this.
      game_beatable = logic.check_requirement_met("Can Reach and Defeat Ganondorf")
      if game_beatable:
        final_progression_sphere = {"Ganon's Tower - Rooftop": "Defeat Ganondorf"}
        progression_spheres.append(final_progression_sphere)
    
    return progression_spheres
