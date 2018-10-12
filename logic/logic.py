
import yaml
import re
from collections import OrderedDict
import copy

import os

from logic.item_types import PROGRESS_ITEMS, NONPROGRESS_ITEMS, CONSUMABLE_ITEMS, DUNGEON_PROGRESS_ITEMS, DUNGEON_NONPROGRESS_ITEMS
from paths import LOGIC_PATH

class Logic:
  DUNGEON_NAMES = OrderedDict([
    ("DRC",  "Dragon Roost Cavern"),
    ("FW",   "Forbidden Woods"),
    ("TotG", "Tower of the Gods"),
    ("FF",   "Forsaken Fortress"),
    ("ET",   "Earth Temple"),
    ("WT",   "Wind Temple"),
  ])
  DUNGEON_NAME_TO_SHORT_DUNGEON_NAME = OrderedDict([v, k] for k, v in DUNGEON_NAMES.items())
  
  PROGRESS_ITEM_GROUPS = OrderedDict([
    ("Triforce Shards",  [
      "Triforce Shard 1",
      "Triforce Shard 2",
      "Triforce Shard 3",
      "Triforce Shard 4",
      "Triforce Shard 5",
      "Triforce Shard 6",
      "Triforce Shard 7",
      "Triforce Shard 8",
    ])
  ])
  
  def __init__(self, rando):
    self.rando = rando
    
    
    # Initialize location related attributes.
    self.item_locations = Logic.load_and_parse_item_locations()
    self.load_and_parse_macros()
    
    self.locations_by_zone_name = OrderedDict()
    for location_name in self.item_locations:
      zone_name, specific_location_name = self.split_location_name_by_zone(location_name)
      if zone_name not in self.locations_by_zone_name:
        self.locations_by_zone_name[zone_name] = []
      self.locations_by_zone_name[zone_name].append(location_name)
    
    self.remaining_item_locations = list(self.item_locations.keys())
    self.prerandomization_dungeon_item_locations = OrderedDict()
    
    self.done_item_locations = OrderedDict()
    for location_name in self.item_locations:
      self.done_item_locations[location_name] = None
    
    self.rock_spire_shop_ship_locations = []
    for location_name, location in self.item_locations.items():
      if location_name.startswith("Rock Spire Isle - Beedle's Special Shop Ship - "):
        self.rock_spire_shop_ship_locations.append(location_name)
    
    # Sync the logic macros with the randomizer.
    self.update_dungeon_entrance_macros()
    self.update_chart_macros()
    self.update_rematch_bosses_macros()
    self.update_sword_mode_macros()
    
    
    # Initialize item related attributes.
    self.all_progress_items = PROGRESS_ITEMS.copy()
    self.all_nonprogress_items = NONPROGRESS_ITEMS.copy()
    self.all_consumable_items = CONSUMABLE_ITEMS.copy()
    
    self.triforce_chart_names = []
    self.treasure_chart_names = []
    for i in range(1, 8+1):
      self.triforce_chart_names.append("Triforce Chart %d" % i)
    for i in range(1, 41+1):
      self.treasure_chart_names.append("Treasure Chart %d" % i)
    
    if self.rando.options.get("sword_mode") == "Swordless":
      self.all_progress_items = [
        item_name for item_name in self.all_progress_items
        if item_name != "Progressive Sword" and item_name != "Hurricane Spin"
      ]
    
    if self.rando.options.get("progression_triforce_charts"):
      self.all_progress_items += self.triforce_chart_names
    else:
      self.all_nonprogress_items += self.triforce_chart_names
    if self.rando.options.get("progression_treasure_charts"):
      self.all_progress_items += self.treasure_chart_names
    else:
      self.all_nonprogress_items += self.treasure_chart_names
    
    # Add dungeon items to the progress/nonprogress items lists.
    if self.rando.options.get("progression_dungeons"):
      self.all_progress_items += DUNGEON_PROGRESS_ITEMS
    else:
      self.all_nonprogress_items += DUNGEON_PROGRESS_ITEMS
    self.all_nonprogress_items += DUNGEON_NONPROGRESS_ITEMS
    
    # Tell the randomizer to register dungeon-specific item names as the normal items.
    for dungeon_item_name in (DUNGEON_PROGRESS_ITEMS + DUNGEON_NONPROGRESS_ITEMS):
      regular_item_name = dungeon_item_name.split(" ", 1)[1]
      self.rando.item_name_to_id[dungeon_item_name] = self.rando.item_name_to_id[regular_item_name]
    
    self.all_cleaned_item_names = []
    for item_name in (self.all_progress_items + self.all_nonprogress_items + self.all_consumable_items):
      cleaned_item_name = self.clean_item_name(item_name)
      if cleaned_item_name not in self.all_cleaned_item_names:
        self.all_cleaned_item_names.append(cleaned_item_name)
    
    self.unplaced_progress_items = self.all_progress_items.copy()
    self.unplaced_nonprogress_items = self.all_nonprogress_items.copy()
    self.unplaced_consumable_items = self.all_consumable_items.copy()
    
    self.progress_item_groups = copy.deepcopy(self.PROGRESS_ITEM_GROUPS)
    
    self.currently_owned_items = []
    
    for item_name in self.rando.starting_items:
      self.add_owned_item(item_name)
    
    self.make_useless_progress_items_nonprogress()
    
    # Replace progress items that are part of a group with the group name instead.
    for group_name, item_names in self.progress_item_groups.items():
      if all(item_name in self.unplaced_progress_items for item_name in item_names):
        self.unplaced_progress_items.append(group_name)
        for item_name in item_names:
          self.unplaced_progress_items.remove(item_name)
    
    # Remove starting items from item groups.
    for group_name, group_item_names in self.progress_item_groups.items():
      items_to_remove_from_group = [
        item_name for item_name in group_item_names
        if item_name in self.rando.starting_items
      ]
      for item_name in items_to_remove_from_group:
        self.progress_item_groups[group_name].remove(item_name)
      if len(self.progress_item_groups[group_name]) == 0:
        if group_name in self.unplaced_progress_items:
          self.unplaced_progress_items.remove(group_name)
  
  def set_location_to_item(self, location_name, item_name):
    #print("Setting %s to %s" % (location_name, item_name))
    
    if self.done_item_locations[location_name]:
      raise Exception("Location was used twice: " + location_name)
    
    self.done_item_locations[location_name] = item_name
    self.remaining_item_locations.remove(location_name)
    
    self.add_owned_item(item_name)
  
  def set_multiple_locations_to_group(self, available_locations, group_items, group_name):    
    if len(available_locations) < len(group_items):
      raise Exception("Not enough locations to place all items in group %s" % group_name)

    for item_name in group_items:
      available_locations = self.filter_locations_valid_for_item(available_locations, item_name)
      location_name = available_locations.pop()
      self.set_location_to_item(location_name, item_name)
    
    self.unplaced_progress_items.remove(group_name)
  
  def set_prerandomization_dungeon_item_location(self, location_name, item_name):
    # Temporarily keep track of where dungeon-specific items are placed before the main progression item randomization loop starts.
    
    #print("Setting prerand %s to %s" % (location_name, item_name))
    
    assert self.is_dungeon_item(item_name)
    assert location_name in self.item_locations
    self.prerandomization_dungeon_item_locations[location_name] = item_name
  
  def get_num_progression_items(self):
    num_progress_items = 0
    for item_name in self.unplaced_progress_items:
      if item_name in self.progress_item_groups:
        group_name = item_name
        for item_name in self.progress_item_groups[group_name]:
          num_progress_items += 1
      else:
        num_progress_items += 1
    
    return num_progress_items
  
  def get_num_progression_locations(self):
    return Logic.get_num_progression_locations_static(self.item_locations, self.rando.options)
  
  @staticmethod
  def get_num_progression_locations_static(item_locations, options):
    progress_locations = Logic.filter_locations_for_progression_static(
      item_locations.keys(),
      item_locations,
      options,
      filter_sunken_treasure=True
    )
    num_progress_locations = len(progress_locations)
    if options.get("progression_triforce_charts"):
      num_progress_locations += 8
    if options.get("progression_treasure_charts"):
      num_progress_locations += 41
    
    return num_progress_locations
  
  def get_progress_and_non_progress_locations(self):
    all_locations = self.item_locations.keys()
    progress_locations = self.filter_locations_for_progression(all_locations, filter_sunken_treasure=True)
    nonprogress_locations = []
    for location_name in all_locations:
      if location_name in progress_locations:
        continue
      
      types = self.item_locations[location_name]["Types"]
      if "Sunken Treasure" in types:
        chart_name = self.chart_name_for_location(location_name)
        if "Triforce Chart" in chart_name:
          if self.rando.options.get("progression_triforce_charts"):
            progress_locations.append(location_name)
          else:
            nonprogress_locations.append(location_name)
        else:
          if self.rando.options.get("progression_treasure_charts"):
            progress_locations.append(location_name)
          else:
            nonprogress_locations.append(location_name)
      else:
        nonprogress_locations.append(location_name)
    
    return (progress_locations, nonprogress_locations)
  
  def add_owned_item(self, item_name):
    cleaned_item_name = self.clean_item_name(item_name)
    if cleaned_item_name not in self.all_cleaned_item_names:
      raise Exception("Unknown item name: " + item_name)
    
    self.currently_owned_items.append(cleaned_item_name)
    
    if item_name in self.unplaced_progress_items:
      self.unplaced_progress_items.remove(item_name)
    elif item_name in self.unplaced_nonprogress_items:
      self.unplaced_nonprogress_items.remove(item_name)
    elif item_name in self.unplaced_consumable_items:
      self.unplaced_consumable_items.remove(item_name)
  
  def remove_owned_item(self, item_name):
    cleaned_item_name = self.clean_item_name(item_name)
    if cleaned_item_name not in self.all_cleaned_item_names:
      raise Exception("Unknown item name: " + item_name)
    
    self.currently_owned_items.remove(cleaned_item_name)
    
    if item_name in self.all_progress_items:
      self.unplaced_progress_items.append(item_name)
    elif item_name in self.all_nonprogress_items:
      self.unplaced_nonprogress_items.append(item_name)
    elif item_name in self.all_consumable_items:
      self.unplaced_consumable_items.append(item_name)
  
  def add_owned_item_or_item_group(self, item_name):
    if item_name in self.progress_item_groups:
      group_name = item_name
      for item_name in self.progress_item_groups[group_name]:
        self.currently_owned_items.append(item_name)
    else:
      self.add_owned_item(item_name)
  
  def remove_owned_item_or_item_group(self, item_name):
    if item_name in self.progress_item_groups:
      group_name = item_name
      for item_name in self.progress_item_groups[group_name]:
        self.currently_owned_items.remove(item_name)
    else:
      self.remove_owned_item(item_name)
  
  def get_accessible_remaining_locations(self, for_progression=False):
    accessible_location_names = []
    
    locations_to_check = self.remaining_item_locations
    if for_progression:
      locations_to_check = self.filter_locations_for_progression(locations_to_check)
    
    for location_name in locations_to_check:
      requirement_expression = self.item_locations[location_name]["Need"]
      if self.check_logical_expression_req(requirement_expression):
        accessible_location_names.append(location_name)
    
    return accessible_location_names
  
  def get_first_useful_item(self, items_to_check, for_progression=False):
    # Searches through a given list of items and returns the first one that opens up at least 1 new location.
    # The randomizer shuffles the list before passing it to this function, so in effect it picks a random useful item.
    
    accessible_undone_locations = self.get_accessible_remaining_locations(for_progression=for_progression)
    inaccessible_undone_item_locations = []
    locations_to_check = self.remaining_item_locations
    if for_progression:
      locations_to_check = self.filter_locations_for_progression(locations_to_check)
    for location_name in locations_to_check:
      if location_name not in accessible_undone_locations:
        inaccessible_undone_item_locations.append(location_name)
    
    # Cache whether each item is useful in order to avoid an absurd number of duplicate recursive calls when checking if a predetermined dungeon item location has a useful item or not.
    self.cached_items_are_useful = {}
    
    for item_name in items_to_check:
      if self.check_item_is_useful(item_name, inaccessible_undone_item_locations):
        self.cached_items_are_useful = None
        return item_name
    
    self.cached_items_are_useful = None
    
    return None
  
  def get_items_by_usefulness_fraction(self, item_names_to_check):
    # Takes a list of items and locations, and determines for each item what the lowest number of items including it the player needs before a new location is opened up, and returns that in a dict.
    # For example, say there are 3 items A B and C, and 2 locations X and Y.
    # Location X requires items A and B while location Y requires items A B and C.
    # This function would return {A: 2, B: 2, C: 3} because A requires 1 other item (B) to help access anything, B also requires one other item (A) to help access anything, but C requires 2 other items (both A and B) before it becomes useful.
    # In other words, items A and B have 1/2 usefulness, while item C has 1/3 usefulness.
    
    accessible_undone_locations = self.get_accessible_remaining_locations(for_progression=True)
    inaccessible_undone_item_locations = []
    locations_to_check = self.remaining_item_locations
    locations_to_check = self.filter_locations_for_progression(locations_to_check)
    for location_name in locations_to_check:
      if location_name not in accessible_undone_locations:
        if location_name in self.prerandomization_dungeon_item_locations:
          # We just ignore items with predetermined dungeon items when calculating usefulness fractions.
          # TODO: In the future, we might want to consider recursively checking if the item here is useful, and if so include this location.
          continue
        inaccessible_undone_item_locations.append(location_name)
    
    # Generate a list of what items are needed for each inaccessible location (+beating the game).
    # Note: Performance could be improved somewhat by only calculating which items are needed for each location at the start of item randomization, instead of once per call to this function. But this seems unnecessary.
    item_names_for_all_locations = []
    for location_name in inaccessible_undone_item_locations:
      requirement_expression = self.item_locations[location_name]["Need"]
      item_names_for_loc = self.get_item_names_from_logical_expression_req(requirement_expression)
      item_names_for_all_locations.append(item_names_for_loc)
    item_names_to_beat_game = self.get_item_names_by_req_name("Can Reach and Defeat Ganondorf")
    item_names_for_all_locations.append(item_names_to_beat_game)
    
    # Now calculate the best case scenario usefulness fraction for all items given.
    item_by_usefulness_fraction = OrderedDict()
    for item_name in item_names_to_check:
      item_by_usefulness_fraction[item_name] = 9999
    
    for item_names_for_loc in item_names_for_all_locations:
      item_names_for_loc_without_owned = item_names_for_loc.copy()
      for item_name in self.currently_owned_items:
        if item_name in item_names_for_loc_without_owned:
          item_names_for_loc_without_owned.remove(item_name)
      
      for item_name in item_names_for_loc_without_owned:
        if item_name not in item_by_usefulness_fraction:
          continue
        usefulness_fraction_for_item = len(item_names_for_loc_without_owned)
        if usefulness_fraction_for_item < item_by_usefulness_fraction[item_name]:
          item_by_usefulness_fraction[item_name] = usefulness_fraction_for_item
    
    return item_by_usefulness_fraction
  
  def get_all_useless_items(self, items_to_check, for_progression=False):
    # Searches through a given list of items and returns which of them do not open up even 1 new location.
    
    if len(items_to_check) == 0:
      return []
    
    accessible_undone_locations = self.get_accessible_remaining_locations(for_progression=for_progression)
    inaccessible_undone_item_locations = []
    locations_to_check = self.remaining_item_locations
    if for_progression:
      locations_to_check = self.filter_locations_for_progression(locations_to_check)
    for location_name in locations_to_check:
      if location_name not in accessible_undone_locations:
        inaccessible_undone_item_locations.append(location_name)
    
    self.cached_items_are_useful = {}
    
    useless_items = []
    for item_name in items_to_check:
      if not self.check_item_is_useful(item_name, inaccessible_undone_item_locations):
        useless_items.append(item_name)
    
    self.cached_items_are_useful = None
    
    return useless_items
  
  def check_item_is_useful(self, item_name, inaccessible_undone_item_locations):
    # Checks whether a specific item unlocks any new locations or not.
    # This function should only be called by get_first_useful_item, get_all_useless_items, or by itself for recursion purposes.
    
    if item_name in self.cached_items_are_useful:
      return self.cached_items_are_useful[item_name]
    
    self.add_owned_item_or_item_group(item_name)
    
    for location_name in inaccessible_undone_item_locations:
      if location_name in self.prerandomization_dungeon_item_locations:
        # If this location has a predetermined dungeon item in it, we need to recursively check if that dungeon item is useful.
        unlocked_prerand_item = self.prerandomization_dungeon_item_locations[location_name]
        # Need to exclude the current location from recursive checks to prevent infinite recursion.
        temp_inaccessible_undone_item_locations = [
          loc for loc in inaccessible_undone_item_locations
          if not loc == location_name
        ]
        if not self.check_item_is_useful(unlocked_prerand_item, temp_inaccessible_undone_item_locations):
          # If that dungeon item is not useful, don't consider the current item useful for unlocking it.
          continue
        
        requirement_expression = self.item_locations[location_name]["Need"]
        if self.check_logical_expression_req(requirement_expression):
          self.remove_owned_item_or_item_group(item_name)
          self.cached_items_are_useful[item_name] = True
          return True
      
      requirement_expression = self.item_locations[location_name]["Need"]
      if self.check_logical_expression_req(requirement_expression):
        self.remove_owned_item_or_item_group(item_name)
        self.cached_items_are_useful[item_name] = True
        return True
    
    self.remove_owned_item_or_item_group(item_name)
    self.cached_items_are_useful[item_name] = False
    return False
  
  def filter_locations_for_progression(self, locations_to_filter, filter_sunken_treasure=False):
    return Logic.filter_locations_for_progression_static(
      locations_to_filter,
      self.item_locations,
      self.rando.options,
      filter_sunken_treasure=filter_sunken_treasure
    )
  
  @staticmethod
  def filter_locations_for_progression_static(locations_to_filter, item_locations, options, filter_sunken_treasure=False):
    filtered_locations = []
    for location_name in locations_to_filter:
      types = item_locations[location_name]["Types"]
      if "No progression" in types:
        continue
      if "Dungeon" in types and not options.get("progression_dungeons"):
        continue
      if "Tingle Chest" in types and not options.get("progression_tingle_chests"):
        continue
      if "Great Fairy" in types and not options.get("progression_great_fairies"):
        continue
      if "Puzzle Secret Cave" in types and not options.get("progression_puzzle_secret_caves"):
        continue
      if "Combat Secret Cave" in types and not options.get("progression_combat_secret_caves"):
        continue
      if "Short Sidequest" in types and not options.get("progression_short_sidequests"):
        continue
      if "Long Sidequest" in types and not options.get("progression_long_sidequests"):
        continue
      if "Spoils Trading" in types and not options.get("progression_spoils_trading"):
        continue
      if "Minigame" in types and not options.get("progression_minigames"):
        continue
      if "Free Gift" in types and not options.get("progression_free_gifts"):
        continue
      if "Mail" in types and not options.get("progression_mail"):
        continue
      if ("Platform" in types or "Raft" in types) and not options.get("progression_platforms_rafts"):
        continue
      if "Submarine" in types and not options.get("progression_submarines"):
        continue
      if "Eye Reef Chest" in types and not options.get("progression_eye_reef_chests"):
        continue
      if ("Big Octo" in types or "Gunboat" in types) and not options.get("progression_big_octos_gunboats"):
        continue
      if "Expensive Purchase" in types and not options.get("progression_expensive_purchases"):
        continue
      if ("Other Chest" in types or "Misc" in types) and not options.get("progression_misc"):
        continue
      if "Sunken Treasure" in types and filter_sunken_treasure:
        continue
      # Note: The Triforce/Treasure Chart sunken treasures are handled differently from other types.
      # During randomization they are handled by not considering the charts themselves to be progress items.
      # That results in the item randomizer considering these locations inaccessible until after all progress items are placed.
      # But when calculating the total number of progression locations, sunken treasures are filtered out entirely here so they can be specially counted elsewhere.
      
      filtered_locations.append(location_name)
    
    return filtered_locations
  
  def check_item_valid_in_location(self, item_name, location_name):
    # Don't allow dungeon items to appear outside their proper dungeon or they wouldn't work correctly.
    if self.is_dungeon_item(item_name) and not self.rando.options.get("keylunacy"):
      short_dungeon_name = item_name.split(" ")[0]
      dungeon_name = self.DUNGEON_NAMES[short_dungeon_name]
      if not self.is_dungeon_location(location_name, dungeon_name_to_match=dungeon_name):
        return False
    
    # Beedle's shop does not work properly if the same item is in multiple slots of the same shop.
    # Ban the Bait Bag slot from having bait.
    if location_name == "The Great Sea - Beedle's Shop Ship - 20 Rupee Item" and item_name in ["All-Purpose Bait", "Hyoi Pear"]:
      return False
    
    # Also ban the same item from appearing more than once in the rock spire shop ship.
    if location_name in self.rock_spire_shop_ship_locations:
      for other_location_name in self.rock_spire_shop_ship_locations:
        if other_location_name == location_name:
          continue
        if other_location_name in self.done_item_locations:
          other_item_name = self.done_item_locations[other_location_name]
          if item_name == other_item_name:
            return False
    
    # Our code to fix Zunari's Magic Armor item gift relies on the items Zunari gives all having different IDs.
    # Therefore we don't allow the other two items Zunari gives to be placed in the Magic Armor slot.
    if location_name == "Windfall Island - Zunari - Stock Exotic Flower in Zunari's Shop" and item_name in ["Town Flower", "Boat's Sail"]:
      return False
    
    return True
  
  def filter_items_by_any_valid_location(self, items, locations):
    # Filters out items that cannot be in any of the given possible locations.
    valid_items = []
    for item_name in items:
      if item_name in self.progress_item_groups:
        group_name = item_name
        items_in_group = self.progress_item_groups[group_name]
        if len(items_in_group) > len(locations):
          # Not enough locations to place all items in this group.
          continue
        # If the number of locations is sufficient, we consider this group able to be placed.
        # NOTE: We do not check if each individual item in the group can also be placed.
        # This is fine for shards and pearls, but would be incorrect for items that actually have location restrictions.
        valid_items.append(group_name)
      else:
        for location_name in locations:
          if self.check_item_valid_in_location(item_name, location_name):
            valid_items.append(item_name)
            break
    return valid_items
  
  def filter_locations_valid_for_item(self, locations, item_name):
    valid_locations = []
    for location_name in locations:
      if self.check_item_valid_in_location(item_name, location_name):
        valid_locations.append(location_name)
    return valid_locations
  
  def filter_items_valid_for_location(self, items, location_name):
    valid_items = []
    for item_name in items:
      if self.check_item_valid_in_location(item_name, location_name):
        valid_items.append(item_name)
    return valid_items
  
  @staticmethod
  def load_and_parse_item_locations():
    with open(os.path.join(LOGIC_PATH, "item_locations.txt")) as f:
      item_locations = yaml.load(f, YamlOrderedDictLoader)
    
    for location_name in item_locations:
      req_string = item_locations[location_name]["Need"]
      if req_string is None:
        # TODO, blank reqs should be an error. Temporarily we will just consider them to be impossible.
        item_locations[location_name]["Need"] = Logic.parse_logic_expression("TODO")
      else:
        item_locations[location_name]["Need"] = Logic.parse_logic_expression(req_string)
      
      types_string = item_locations[location_name]["Types"]
      types = types_string.split(",")
      types = [type.strip() for type in types]
      item_locations[location_name]["Types"] = types
    
    return item_locations
    
  def load_and_parse_macros(self):
    with open(os.path.join(LOGIC_PATH, "macros.txt")) as f:
      macro_strings = yaml.safe_load(f)
    self.macros = {}
    for macro_name, req_string in macro_strings.items():
      self.set_macro(macro_name, req_string)
  
  def set_macro(self, macro_name, req_string):
    self.macros[macro_name] = Logic.parse_logic_expression(req_string)
  
  def update_dungeon_entrance_macros(self):
    # Update all the dungeon access macros to take randomized entrances into account.
    for entrance_name, dungeon_name in self.rando.dungeon_entrances.items():
      dungeon_access_macro_name = "Can Access " + dungeon_name
      dungeon_entrance_access_macro_name = "Can Access " + entrance_name
      self.set_macro(dungeon_access_macro_name, dungeon_entrance_access_macro_name)
  
  def temporarily_make_dungeon_entrance_macros_impossible(self):
    # Update all the dungeon access macros to be considered "Impossible".
    # Useful when the dungeon entrance randomizer is selecting which dungeons should be allowed where.
    for entrance_name, dungeon_name in self.rando.dungeon_entrances.items():
      dungeon_access_macro_name = "Can Access " + dungeon_name
      self.set_macro(dungeon_access_macro_name, "Impossible")
  
  def temporarily_make_dungeon_entrance_macros_worst_case_scenario(self):
    # Update all the dungeon access macros to be a combination of all the macros for accessing dungeons that can have their entrance randomized.
    all_dungeon_entrance_access_macro_names = []
    for entrance_name, dungeon_name in self.rando.dungeon_entrances.items():
      dungeon_entrance_access_macro_name = "Can Access " + entrance_name
      all_dungeon_entrance_access_macro_names.append(dungeon_entrance_access_macro_name)
    can_access_all_dungeon_entrances = " & ".join(all_dungeon_entrance_access_macro_names)
    for entrance_name, dungeon_name in self.rando.dungeon_entrances.items():
      dungeon_access_macro_name = "Can Access " + dungeon_name
      self.set_macro(dungeon_access_macro_name, can_access_all_dungeon_entrances)
  
  def update_chart_macros(self):
    # Update all the "Chart for Island" macros to take randomized charts into account.
    for island_number in range(1, 49+1):
      chart_macro_name = "Chart for Island %d" % island_number
      chart_item_name = self.rando.island_number_to_chart_name[island_number]
      
      if "Triforce Chart" in chart_item_name:
        req_string = "%s & Any Wallet Upgrade" % chart_item_name
      else:
        req_string = chart_item_name
      
      self.set_macro(chart_macro_name, req_string)
  
  def update_rematch_bosses_macros(self):
    if self.rando.options.get("skip_rematch_bosses"):
      self.set_macro("Can Unlock Ganon's Tower Four Boss Door", "Nothing")
    else:
      self.set_macro("Can Unlock Ganon's Tower Four Boss Door", "Can Complete All Memory Dungeons and Bosses")
  
  def update_sword_mode_macros(self):
    if self.rando.options.get("sword_mode") == "Swordless":
      self.set_macro("Can Sword Fight with Orca", "Can Sword Fight with Orca in Swordless")
      self.set_macro("Can Defeat Phantom Ganon", "Can Defeat Phantom Ganon in Swordless")
      self.set_macro("Can Access Hyrule", "Can Access Hyrule in Swordless")
      self.set_macro("Can Defeat Ganondorf", "Can Defeat Ganondorf in Swordless")
    else:
      self.set_macro("Can Sword Fight with Orca", "Can Sword Fight with Orca Outside Swordless")
      self.set_macro("Can Defeat Phantom Ganon", "Can Defeat Phantom Ganon Outside Swordless")
      self.set_macro("Can Access Hyrule", "Can Access Hyrule Outside Swordless")
      self.set_macro("Can Defeat Ganondorf", "Can Defeat Ganondorf Outside Swordless")
  
  def clean_item_name(self, item_name):
    # Remove parentheses from any item names that may have them. (Formerly Master Swords, though that's not an issue anymore.)
    return item_name.replace("(", "").replace(")", "")
  
  def make_useless_progress_items_nonprogress(self):
    # Detect which progress items don't actually help access any locations with the user's current settings, and move those over to the nonprogress item list instead.
    # This is so things like dungeons-only runs don't have a lot of useless items hogging the progress locations.
    
    if self.rando.options.get("randomize_dungeon_entrances"):
      # Since the randomizer hasn't decided which dungeon will be where yet, we have to assume the worst case scenario by considering that you need to be able to access all dungeon entrances in order to access each individual dungeon.
      self.temporarily_make_dungeon_entrance_macros_worst_case_scenario()
    
    filter_sunken_treasure = True
    if self.rando.options.get("progression_triforce_charts") or self.rando.options.get("progression_treasure_charts"):
      filter_sunken_treasure = False
    progress_locations = Logic.filter_locations_for_progression_static(
      self.item_locations.keys(),
      self.item_locations,
      self.rando.options,
      filter_sunken_treasure=filter_sunken_treasure
    )
    
    useful_items = []
    for location_name in progress_locations:
      requirement_expression = self.item_locations[location_name]["Need"]
      useful_items += self.get_item_names_from_logical_expression_req(requirement_expression)
    useful_items += self.get_item_names_by_req_name("Can Reach and Defeat Ganondorf")
    
    all_progress_items_filtered = []
    for item_name in useful_items:
      if item_name == "Progressive Sword" and self.rando.options.get("sword_mode") == "Swordless":
        continue
      if self.is_dungeon_item(item_name) and not self.rando.options.get("progression_dungeons"):
        continue
      if item_name not in self.all_progress_items:
        if not (item_name.startswith("Triforce Chart ") or item_name.startswith("Treasure Chart")):
          raise Exception("Item %s opens up progress locations but is not in the list of all progress items." % item_name)
      if item_name in all_progress_items_filtered:
        # Avoid duplicates
        continue
      all_progress_items_filtered.append(item_name)
    
    items_to_make_nonprogress = [
      item_name for item_name in self.all_progress_items
      if item_name not in all_progress_items_filtered
      and item_name not in self.currently_owned_items
    ]
    for item_name in items_to_make_nonprogress:
      #print(item_name)
      self.all_progress_items.remove(item_name)
      self.all_nonprogress_items.append(item_name)
      self.unplaced_progress_items.remove(item_name)
      self.unplaced_nonprogress_items.append(item_name)
    
    if self.rando.options.get("randomize_dungeon_entrances"):
      # Reset the dungeon access macros if we changed them earlier.
      self.update_dungeon_entrance_macros()
  
  def split_location_name_by_zone(self, location_name):
    if " - " in location_name:
      zone_name, specific_location_name = location_name.split(" - ", 1)
    else:
      zone_name = specific_location_name = location_name
    
    return zone_name, specific_location_name
  
  def is_dungeon_item(self, item_name):
    return (item_name in DUNGEON_PROGRESS_ITEMS or item_name in DUNGEON_NONPROGRESS_ITEMS)
  
  def is_dungeon_location(self, location_name, dungeon_name_to_match=None):
    zone_name, specific_location_name = self.split_location_name_by_zone(location_name)
    if zone_name not in self.DUNGEON_NAME_TO_SHORT_DUNGEON_NAME:
      # Not a dungeon.
      return False
    if dungeon_name_to_match and dungeon_name_to_match != zone_name:
      # Wrong dungeon.
      return False
    if "Sunken Treasure" in self.item_locations[location_name]["Types"]:
      # Outside the dungeon.
      return False
    return True
  
  @staticmethod
  def parse_logic_expression(string):
    tokens = [str.strip() for str in re.split("([&|()])", string)]
    tokens = [token for token in tokens if token != ""]
    
    stack = []
    for token in tokens:
      if token == "(":
        stack.append("(")
      elif token == ")":
        nested_tokens = []
        
        nested_parentheses_level = 0
        while len(stack) != 0:
          exp = stack.pop()
          if exp == "(":
            if nested_parentheses_level == 0:
              break
            else:
              nested_parentheses_level -= 1
          if exp == ")":
            nested_parentheses_level += 1
          nested_tokens.append(exp)
        
        nested_tokens.reverse()
        stack.append("(")
        stack.append(nested_tokens)
        stack.append(")")
      else:
        stack.append(token)
    
    return stack
  
  def check_requirement_met(self, req_name):
    if req_name.startswith("Progressive "):
      return self.check_progressive_item_req(req_name)
    elif " Small Key x" in req_name:
      return self.check_small_key_req(req_name)
    elif req_name.startswith("Can Access Other Location \""):
      return self.check_other_location_requirement(req_name)
    elif req_name in self.all_cleaned_item_names:
      return req_name in self.currently_owned_items
    elif req_name in self.macros:
      logical_expression = self.macros[req_name]
      return self.check_logical_expression_req(logical_expression)
    elif req_name == "Nothing":
      return True
    elif req_name == "Impossible":
      return False
    else:
      raise Exception("Unknown requirement name: " + req_name)
  
  def check_logical_expression_req(self, logical_expression):
    expression_type = None
    subexpression_results = []
    tokens = logical_expression.copy()
    tokens.reverse()
    while tokens:
      token = tokens.pop()
      if token == "|":
        if expression_type == "AND":
          raise Exception("Error parsing progression requirements: & and | must not be within the same nesting level.")
        expression_type = "OR"
      elif token == "&":
        if expression_type == "OR":
          raise Exception("Error parsing progression requirements: & and | must not be within the same nesting level.")
        expression_type = "AND"
      elif token == "(":
        nested_expression = tokens.pop()
        if nested_expression == "(":
          # Nested parentheses
          nested_expression = ["("] + tokens.pop()
        result = self.check_logical_expression_req(nested_expression)
        subexpression_results.append(result)
        assert tokens.pop() == ")"
      else:
        # Subexpression.
        result = self.check_requirement_met(token)
        subexpression_results.append(result)
    
    if expression_type == "OR":
      return any(subexpression_results)
    else:
      return all(subexpression_results)
  
  def get_item_names_by_req_name(self, req_name):
    item_names = []
    if req_name.startswith("Progressive "):
      match = re.search(r"^(Progressive .+) x(\d+)$", req_name)
      item_name = match.group(1)
      num_required = int(match.group(2))
      for i in range(num_required):
        item_names.append(item_name)
    elif " Small Key x" in req_name:
      match = re.search(r"^(.+ Small Key) x(\d+)$", req_name)
      small_key_name = match.group(1)
      num_keys_required = int(match.group(2))
      for i in range(num_keys_required):
        item_names.append(small_key_name)
    elif req_name.startswith("Can Access Other Location \""):
      match = re.search(r"^Can Access Other Location \"([^\"]+)\"$", req_name)
      other_location_name = match.group(1)
      requirement_expression = self.item_locations[other_location_name]["Need"]
      item_names += self.get_item_names_from_logical_expression_req(requirement_expression)
    elif req_name in self.all_cleaned_item_names:
      item_names.append(req_name)
    elif req_name in self.macros:
      logical_expression = self.macros[req_name]
      item_names += self.get_item_names_from_logical_expression_req(logical_expression)
    elif req_name == "Nothing":
      pass
    elif req_name == "Impossible":
      pass
    else:
      raise Exception("Unknown requirement name: " + req_name)
    
    return item_names
  
  def get_item_names_from_logical_expression_req(self, logical_expression):
    if self.check_logical_expression_req(logical_expression):
      # If this expression is already satisfied, we don't want to include any other items in the OR statement.
      return []
    
    item_names = []
    tokens = logical_expression.copy()
    tokens.reverse()
    while tokens:
      token = tokens.pop()
      if token == "|":
        pass
      elif token == "&":
        pass
      elif token == "(":
        nested_expression = tokens.pop()
        if nested_expression == "(":
          # Nested parentheses
          nested_expression = ["("] + tokens.pop()
        result = self.get_item_names_from_logical_expression_req(nested_expression)
        item_names += result
        assert tokens.pop() == ")"
      else:
        # Subexpression.
        sub_item_names = self.get_item_names_by_req_name(token)
        item_names += sub_item_names
    
    return item_names
  
  def check_progressive_item_req(self, req_name):
    match = re.search(r"^(Progressive .+) x(\d+)$", req_name)
    item_name = match.group(1)
    num_required = int(match.group(2))
    
    num_owned = self.currently_owned_items.count(item_name)
    return num_owned >= num_required
  
  def check_small_key_req(self, req_name):
    match = re.search(r"^(.+ Small Key) x(\d+)$", req_name)
    small_key_name = match.group(1)
    num_keys_required = int(match.group(2))
    
    num_small_keys_owned = self.currently_owned_items.count(small_key_name)
    return num_small_keys_owned >= num_keys_required
  
  def check_other_location_requirement(self, req_name):
    match = re.search(r"^Can Access Other Location \"([^\"]+)\"$", req_name)
    other_location_name = match.group(1)
    
    requirement_expression = self.item_locations[other_location_name]["Need"]
    return self.check_logical_expression_req(requirement_expression)
  
  def chart_name_for_location(self, location_name):
    reqs = self.item_locations[location_name]["Need"]
    chart_req = next(req for req in reqs if req.startswith("Chart for Island "))
    
    reqs = self.macros[chart_req]
    chart_name = reqs[0]
    assert chart_name in self.all_cleaned_item_names
    
    return chart_name

class YamlOrderedDictLoader(yaml.SafeLoader):
  pass

YamlOrderedDictLoader.add_constructor(
  yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
  lambda loader, node: OrderedDict(loader.construct_pairs(node))
)
