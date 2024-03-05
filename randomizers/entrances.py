from dataclasses import dataclass, KW_ONLY
import re
from typing import ClassVar
from collections import defaultdict

from wwlib.dzx import DZx, _2DMA, ACTR, PLYR, SCLS, STAG
from wwlib.events import EventList
from randomizers.base_randomizer import BaseRandomizer
from options.wwrando_options import EntranceMixMode

@dataclass(frozen=True)
class ZoneEntrance:
  stage_name: str
  room_num: int
  scls_exit_index: int
  spawn_id: int
  entrance_name: str
  island_name: str = None
  warp_out_stage_name: str = None
  warp_out_room_num: int = None
  warp_out_spawn_id: int = None
  nested_in: 'ZoneExit' = None
  
  @property
  def is_nested(self):
    return self.nested_in is not None
  
  def __repr__(self):
    return f"ZoneEntrance('{self.entrance_name}')"
  
  all: ClassVar[dict[str, 'ZoneEntrance']] = {}
  
  def __post_init__(self):
    ZoneEntrance.all[self.entrance_name] = self
    
    # Must be an island entrance XOR must be a nested entrance.
    assert (self.island_name is None) ^ (self.nested_in is None)
    assert (self.warp_out_stage_name is None) ^ (self.nested_in is None)

@dataclass(frozen=True)
class ZoneExit:
  stage_name: str
  room_num: int
  scls_exit_index: int
  spawn_id: int
  unique_name: str
  _: KW_ONLY
  boss_stage_name: str = None
  zone_name: str = None
  # If zone_name is specified, this exit will assume by default that it owns all item locations in
  # that zone which are behind randomizable entrances. If a single zone has multiple randomizable
  # entrances, only one of them at most can use zone_name. The rest must have their item locations
  # explicitly specified using ITEM_LOCATION_NAME_TO_EXIT_OVERRIDES.
  
  def __repr__(self):
    return f"ZoneExit('{self.unique_name}')"
  
  all: ClassVar[dict[str, 'ZoneExit']] = {}
  
  def __post_init__(self):
    ZoneExit.all[self.unique_name] = self

DUNGEON_ENTRANCES = [
  ZoneEntrance("Adanmae", 0, 2, 2, "Dungeon Entrance on Dragon Roost Island", "Dragon Roost Island", "sea", 13, 211),
  ZoneEntrance("sea", 41, 6, 6, "Dungeon Entrance in Forest Haven Sector", "Forest Haven", "Omori", 0, 215),
  ZoneEntrance("sea", 26, 0, 2, "Dungeon Entrance in Tower of the Gods Sector", "Tower of the Gods Sector", "sea", 26, 1),
  # ZoneEntrance("sea", 1, None, None, "Dungeon Entrance in Forsaken Fortress Sector", "Forsaken Fortress Sector", "sea", 1, 0),
  ZoneEntrance("Edaichi", 0, 0, 1, "Dungeon Entrance on Headstone Island", "Headstone Island", "sea", 45, 229),
  ZoneEntrance("Ekaze", 0, 0, 1, "Dungeon Entrance on Gale Isle", "Gale Isle", "sea", 4, 232),
]
DUNGEON_EXITS = [
  ZoneExit("M_NewD2", 0, 0, 0, "Dragon Roost Cavern", boss_stage_name="M_DragB", zone_name="Dragon Roost Cavern"),
  ZoneExit("kindan", 0, 0, 0, "Forbidden Woods", boss_stage_name="kinBOSS", zone_name="Forbidden Woods"),
  ZoneExit("Siren", 0, 1, 0, "Tower of the Gods", boss_stage_name="SirenB", zone_name="Tower of the Gods"),
  # ZoneExit("sea", 1, None, None, "Forsaken Fortress", boss_stage_name="M2tower", zone_name="Forsaken Fortress"),
  ZoneExit("M_Dai", 0, 0, 0, "Earth Temple", boss_stage_name="M_DaiB", zone_name="Earth Temple"),
  ZoneExit("kaze", 15, 0, 15, "Wind Temple", boss_stage_name="kazeB", zone_name="Wind Temple"),
]

MINIBOSS_ENTRANCES = [
  ZoneEntrance("kindan", 9, 0, 1, "Miniboss Entrance in Forbidden Woods", nested_in=ZoneExit.all["Forbidden Woods"]),
  ZoneEntrance("Siren", 14, 0, 1, "Miniboss Entrance in Tower of the Gods", nested_in=ZoneExit.all["Tower of the Gods"]),
  ZoneEntrance("M_Dai", 7, 0, 9, "Miniboss Entrance in Earth Temple", nested_in=ZoneExit.all["Earth Temple"]),
  ZoneEntrance("kaze", 2, 3, 20, "Miniboss Entrance in Wind Temple", nested_in=ZoneExit.all["Wind Temple"]),
  ZoneEntrance("Hyroom", 0, 2, 2, "Miniboss Entrance in Hyrule Castle", "Tower of the Gods Sector", "Hyroom", 0, 10),
]
MINIBOSS_EXITS = [
  ZoneExit("kinMB", 10, 0, 0, "Forbidden Woods Miniboss Arena"),
  ZoneExit("SirenMB", 23, 0, 0, "Tower of the Gods Miniboss Arena"),
  ZoneExit("M_DaiMB", 12, 0, 0, "Earth Temple Miniboss Arena"),
  ZoneExit("kazeMB", 6, 0, 0, "Wind Temple Miniboss Arena"),
  ZoneExit("kenroom", 0, 0, 0, "Master Sword Chamber"),
]

BOSS_ENTRANCES = [
  ZoneEntrance("M_NewD2", 10, 1, 27, "Boss Entrance in Dragon Roost Cavern", nested_in=ZoneExit.all["Dragon Roost Cavern"]),
  ZoneEntrance("kindan", 16, 0, 1, "Boss Entrance in Forbidden Woods", nested_in=ZoneExit.all["Forbidden Woods"]),
  ZoneEntrance("Siren", 18, 0, 27, "Boss Entrance in Tower of the Gods", nested_in=ZoneExit.all["Tower of the Gods"]),
  ZoneEntrance("sea", 1, 16, 27, "Boss Entrance in Forsaken Fortress", "Forsaken Fortress Sector", "sea", 1, 0),
  ZoneEntrance("M_Dai", 15, 0, 27, "Boss Entrance in Earth Temple", nested_in=ZoneExit.all["Earth Temple"]),
  ZoneEntrance("kaze", 12, 0, 27, "Boss Entrance in Wind Temple", nested_in=ZoneExit.all["Wind Temple"]),
]
BOSS_EXITS = [
  ZoneExit("M_DragB", 0, None, 0, "Gohma Boss Arena"),
  ZoneExit("kinBOSS", 0, None, 0, "Kalle Demos Boss Arena"),
  ZoneExit("SirenB", 0, None, 0, "Gohdan Boss Arena"),
  ZoneExit("M2tower", 0, None, 16, "Helmaroc King Boss Arena"),
  ZoneExit("M_DaiB", 0, None, 0, "Jalhalla Boss Arena"),
  ZoneExit("kazeB", 0, None, 0, "Molgera Boss Arena"),
]

SECRET_CAVE_ENTRANCES = [
  ZoneEntrance("sea", 44, 8, 10, "Secret Cave Entrance on Outset Island", "Outset Island", "sea", 44, 10),
  ZoneEntrance("sea", 13, 2, 5, "Secret Cave Entrance on Dragon Roost Island", "Dragon Roost Island", "sea", 13, 5),
  # Note: For Fire Mountain and Ice Ring Isle, the spawn ID specified is on the sea with KoRL
  # instead of being at the cave entrance, since the player would get burnt/frozen if they were put
  # at the entrance while the island is still active.
  ZoneEntrance("sea", 20, 0, 0, "Secret Cave Entrance on Fire Mountain", "Fire Mountain", "sea", 20, 0),
  ZoneEntrance("sea", 40, 0, 0, "Secret Cave Entrance on Ice Ring Isle", "Ice Ring Isle", "sea", 40, 0),
  ZoneEntrance("Abesso", 0, 1, 1, "Secret Cave Entrance on Private Oasis", "Private Oasis", "Abesso", 0, 1),
  ZoneEntrance("sea", 29, 0, 5, "Secret Cave Entrance on Needle Rock Isle", "Needle Rock Isle", "sea", 29, 5),
  ZoneEntrance("sea", 47, 1, 5, "Secret Cave Entrance on Angular Isles", "Angular Isles", "sea", 47, 5),
  ZoneEntrance("sea", 48, 0, 5, "Secret Cave Entrance on Boating Course", "Boating Course", "sea", 48, 5),
  ZoneEntrance("sea", 31, 0, 1, "Secret Cave Entrance on Stone Watcher Island", "Stone Watcher Island", "sea", 31, 1),
  ZoneEntrance("sea", 7, 0, 1, "Secret Cave Entrance on Overlook Island", "Overlook Island", "sea", 7, 1),
  ZoneEntrance("sea", 35, 0, 1, "Secret Cave Entrance on Bird's Peak Rock", "Bird's Peak Rock", "sea", 35, 1),
  ZoneEntrance("sea", 12, 0, 1, "Secret Cave Entrance on Pawprint Isle", "Pawprint Isle", "sea", 12, 1),
  ZoneEntrance("sea", 12, 1, 5, "Secret Cave Entrance on Pawprint Isle Side Isle", "Pawprint Isle", "sea", 12, 5),
  ZoneEntrance("sea", 36, 0, 1, "Secret Cave Entrance on Diamond Steppe Island", "Diamond Steppe Island", "sea", 36, 1),
  ZoneEntrance("sea", 34, 0, 1, "Secret Cave Entrance on Bomb Island", "Bomb Island", "sea", 34, 1),
  ZoneEntrance("sea", 16, 0, 1, "Secret Cave Entrance on Rock Spire Isle", "Rock Spire Isle", "sea", 16, 1),
  ZoneEntrance("sea", 38, 0, 5, "Secret Cave Entrance on Shark Island", "Shark Island", "sea", 38, 5),
  ZoneEntrance("sea", 42, 0, 2, "Secret Cave Entrance on Cliff Plateau Isles", "Cliff Plateau Isles", "sea", 42, 2),
  ZoneEntrance("sea", 43, 0, 5, "Secret Cave Entrance on Horseshoe Island", "Horseshoe Island", "sea", 43, 5),
  ZoneEntrance("sea", 2, 0, 1, "Secret Cave Entrance on Star Island", "Star Island", "sea", 2, 1),
]
SECRET_CAVE_EXITS = [
  ZoneExit("Cave09", 0, 1, 0, "Savage Labyrinth", zone_name="Outset Island"),
  ZoneExit("TF_06", 0, 0, 0, "Dragon Roost Island Secret Cave", zone_name="Dragon Roost Island"),
  ZoneExit("MiniKaz", 0, 0, 0, "Fire Mountain Secret Cave", zone_name="Fire Mountain"),
  ZoneExit("MiniHyo", 0, 0, 0, "Ice Ring Isle Secret Cave", zone_name="Ice Ring Isle"),
  ZoneExit("TF_04", 0, 0, 0, "Cabana Labyrinth", zone_name="Private Oasis"),
  ZoneExit("SubD42", 0, 0, 0, "Needle Rock Isle Secret Cave", zone_name="Needle Rock Isle"),
  ZoneExit("SubD43", 0, 0, 0, "Angular Isles Secret Cave", zone_name="Angular Isles"),
  ZoneExit("SubD71", 0, 0, 0, "Boating Course Secret Cave", zone_name="Boating Course"),
  ZoneExit("TF_01", 0, 0, 0, "Stone Watcher Island Secret Cave", zone_name="Stone Watcher Island"),
  ZoneExit("TF_02", 0, 0, 0, "Overlook Island Secret Cave", zone_name="Overlook Island"),
  ZoneExit("TF_03", 0, 0, 0, "Bird's Peak Rock Secret Cave", zone_name="Bird's Peak Rock"),
  ZoneExit("TyuTyu", 0, 0, 0, "Pawprint Isle Chuchu Cave", zone_name="Pawprint Isle"),
  ZoneExit("Cave07", 0, 0, 0, "Pawprint Isle Wizzrobe Cave"),
  ZoneExit("WarpD", 0, 0, 0, "Diamond Steppe Island Warp Maze Cave", zone_name="Diamond Steppe Island"),
  ZoneExit("Cave01", 0, 0, 0, "Bomb Island Secret Cave", zone_name="Bomb Island"),
  ZoneExit("Cave04", 0, 0, 0, "Rock Spire Isle Secret Cave", zone_name="Rock Spire Isle"),
  ZoneExit("ITest63", 0, 0, 0, "Shark Island Secret Cave", zone_name="Shark Island"),
  ZoneExit("Cave03", 0, 0, 0, "Cliff Plateau Isles Secret Cave", zone_name="Cliff Plateau Isles"),
  ZoneExit("Cave05", 0, 0, 0, "Horseshoe Island Secret Cave", zone_name="Horseshoe Island"),
  ZoneExit("Cave02", 0, 0, 0, "Star Island Secret Cave", zone_name="Star Island"),
]

SECRET_CAVE_INNER_ENTRANCES = [
  ZoneEntrance("MiniHyo", 0, 1, 0, "Inner Entrance in Ice Ring Isle Secret Cave", nested_in=ZoneExit.all["Ice Ring Isle Secret Cave"]),
  ZoneEntrance("Cave03", 0, 1, 1, "Inner Entrance in Cliff Plateau Isles Secret Cave", nested_in=ZoneExit.all["Cliff Plateau Isles Secret Cave"]),
]
SECRET_CAVE_INNER_EXITS = [
  ZoneExit("ITest62", 0, 0, 0, "Ice Ring Isle Inner Cave"),
  ZoneExit("sea", 42, 1, 1, "Cliff Plateau Isles Inner Cave"),
]

FAIRY_FOUNTAIN_ENTRANCES = [
  ZoneEntrance("A_mori", 0, 1, 2, "Fairy Fountain Entrance on Outset Island", "Outset Island", "A_mori", 0, 2),
  ZoneEntrance("sea", 28, 0, 1, "Fairy Fountain Entrance on Thorned Fairy Island", "Thorned Fairy Island", "sea", 28, 1),
  ZoneEntrance("sea", 19, 0, 1, "Fairy Fountain Entrance on Eastern Fairy Island", "Eastern Fairy Island", "sea", 19, 1),
  ZoneEntrance("sea", 15, 0, 1, "Fairy Fountain Entrance on Western Fairy Island", "Western Fairy Island", "sea", 15, 1),
  ZoneEntrance("sea", 39, 0, 1, "Fairy Fountain Entrance on Southern Fairy Island", "Southern Fairy Island", "sea", 39, 1),
  ZoneEntrance("sea", 3, 0, 1, "Fairy Fountain Entrance on Northern Fairy Island", "Northern Fairy Island", "sea", 3, 1),
]
FAIRY_FOUNTAIN_EXITS = [
  ZoneExit("Fairy04", 0, 0, 0, "Outset Fairy Fountain"),
  ZoneExit("Fairy05", 0, 0, 0, "Thorned Fairy Fountain", zone_name="Thorned Fairy Island"),
  ZoneExit("Fairy02", 0, 0, 0, "Eastern Fairy Fountain", zone_name="Eastern Fairy Island"),
  ZoneExit("Fairy03", 0, 0, 0, "Western Fairy Fountain", zone_name="Western Fairy Island"),
  ZoneExit("Fairy06", 0, 0, 0, "Southern Fairy Fountain", zone_name="Southern Fairy Island"),
  ZoneExit("Fairy01", 0, 0, 0, "Northern Fairy Fountain", zone_name="Northern Fairy Island"),
]


DUNGEON_ENTRANCE_NAMES_WITH_NO_REQUIREMENTS = [
  "Dungeon Entrance on Dragon Roost Island",
]
SECRET_CAVE_ENTRANCE_NAMES_WITH_NO_REQUIREMENTS = [
  "Secret Cave Entrance on Pawprint Isle",
  "Secret Cave Entrance on Cliff Plateau Isles",
]

DUNGEON_EXIT_NAMES_WITH_NO_REQUIREMENTS = [
  "Dragon Roost Cavern",
]
PUZZLE_SECRET_CAVE_EXIT_NAMES_WITH_NO_REQUIREMENTS = [
  "Pawprint Isle Chuchu Cave",
  "Ice Ring Isle Secret Cave",
  "Bird's Peak Rock Secret Cave", # Technically this has requirements, but it's just Wind Waker+Wind's Requiem.
  "Diamond Steppe Island Warp Maze Cave",
]
COMBAT_SECRET_CAVE_EXIT_NAMES_WITH_NO_REQUIREMENTS = [
  "Rock Spire Isle Secret Cave",
]

ENTRANCE_RANDOMIZABLE_ITEM_LOCATION_TYPES = [
  "Dungeon",
  "Puzzle Secret Cave",
  "Combat Secret Cave",
  "Savage Labyrinth",
  "Great Fairy",
]
ITEM_LOCATION_NAME_TO_EXIT_OVERRIDES = {
  "Forbidden Woods - Mothula Miniboss Room"          : ZoneExit.all["Forbidden Woods Miniboss Arena"],
  "Tower of the Gods - Darknut Miniboss Room"        : ZoneExit.all["Tower of the Gods Miniboss Arena"],
  "Earth Temple - Stalfos Miniboss Room"             : ZoneExit.all["Earth Temple Miniboss Arena"],
  "Wind Temple - Wizzrobe Miniboss Room"             : ZoneExit.all["Wind Temple Miniboss Arena"],
  "Hyrule - Master Sword Chamber"                    : ZoneExit.all["Master Sword Chamber"],
  
  "Dragon Roost Cavern - Gohma Heart Container"      : ZoneExit.all["Gohma Boss Arena"],
  "Forbidden Woods - Kalle Demos Heart Container"    : ZoneExit.all["Kalle Demos Boss Arena"],
  "Tower of the Gods - Gohdan Heart Container"       : ZoneExit.all["Gohdan Boss Arena"],
  "Forsaken Fortress - Helmaroc King Heart Container": ZoneExit.all["Helmaroc King Boss Arena"],
  "Earth Temple - Jalhalla Heart Container"          : ZoneExit.all["Jalhalla Boss Arena"],
  "Wind Temple - Molgera Heart Container"            : ZoneExit.all["Molgera Boss Arena"],
  
  "Pawprint Isle - Wizzrobe Cave"                    : ZoneExit.all["Pawprint Isle Wizzrobe Cave"],
  
  "Ice Ring Isle - Inner Cave - Chest"               : ZoneExit.all["Ice Ring Isle Inner Cave"],
  "Cliff Plateau Isles - Highest Isle"               : ZoneExit.all["Cliff Plateau Isles Inner Cave"],
  
  "Outset Island - Great Fairy"                      : ZoneExit.all["Outset Fairy Fountain"],
}

class EntranceRandomizer(BaseRandomizer):
  def __init__(self, rando):
    super().__init__(rando)
    
    self.item_location_name_to_zone_exit: dict[str, ZoneExit] = {}
    self.zone_exit_to_item_location_names: dict[ZoneExit, list[str]] = defaultdict(list)
    for loc_name in self.logic.item_locations:
      zone_exit = self.get_zone_exit_for_item_location(loc_name)
      if zone_exit is None:
        continue
      self.item_location_name_to_zone_exit[loc_name] = zone_exit
      self.zone_exit_to_item_location_names[zone_exit].append(loc_name)
    
    # Default entrances connections to be used if the entrance randomizer is not on.
    self.entrance_connections = {
      "Dungeon Entrance on Dragon Roost Island": "Dragon Roost Cavern",
      "Dungeon Entrance in Forest Haven Sector": "Forbidden Woods",
      "Dungeon Entrance in Tower of the Gods Sector": "Tower of the Gods",
      # "Dungeon Entrance in Forsaken Fortress Sector": "Forsaken Fortress",
      "Dungeon Entrance on Headstone Island": "Earth Temple",
      "Dungeon Entrance on Gale Isle": "Wind Temple",
      
      "Miniboss Entrance in Forbidden Woods": "Forbidden Woods Miniboss Arena",
      "Miniboss Entrance in Tower of the Gods": "Tower of the Gods Miniboss Arena",
      "Miniboss Entrance in Earth Temple": "Earth Temple Miniboss Arena",
      "Miniboss Entrance in Wind Temple": "Wind Temple Miniboss Arena",
      "Miniboss Entrance in Hyrule Castle": "Master Sword Chamber",
      
      "Boss Entrance in Dragon Roost Cavern": "Gohma Boss Arena",
      "Boss Entrance in Forbidden Woods": "Kalle Demos Boss Arena",
      "Boss Entrance in Tower of the Gods": "Gohdan Boss Arena",
      "Boss Entrance in Forsaken Fortress": "Helmaroc King Boss Arena",
      "Boss Entrance in Earth Temple": "Jalhalla Boss Arena",
      "Boss Entrance in Wind Temple": "Molgera Boss Arena",
      
      "Secret Cave Entrance on Outset Island": "Savage Labyrinth",
      "Secret Cave Entrance on Dragon Roost Island": "Dragon Roost Island Secret Cave",
      "Secret Cave Entrance on Fire Mountain": "Fire Mountain Secret Cave",
      "Secret Cave Entrance on Ice Ring Isle": "Ice Ring Isle Secret Cave",
      "Secret Cave Entrance on Private Oasis": "Cabana Labyrinth",
      "Secret Cave Entrance on Needle Rock Isle": "Needle Rock Isle Secret Cave",
      "Secret Cave Entrance on Angular Isles": "Angular Isles Secret Cave",
      "Secret Cave Entrance on Boating Course": "Boating Course Secret Cave",
      "Secret Cave Entrance on Stone Watcher Island": "Stone Watcher Island Secret Cave",
      "Secret Cave Entrance on Overlook Island": "Overlook Island Secret Cave",
      "Secret Cave Entrance on Bird's Peak Rock": "Bird's Peak Rock Secret Cave",
      "Secret Cave Entrance on Pawprint Isle": "Pawprint Isle Chuchu Cave",
      "Secret Cave Entrance on Pawprint Isle Side Isle": "Pawprint Isle Wizzrobe Cave",
      "Secret Cave Entrance on Diamond Steppe Island": "Diamond Steppe Island Warp Maze Cave",
      "Secret Cave Entrance on Bomb Island": "Bomb Island Secret Cave",
      "Secret Cave Entrance on Rock Spire Isle": "Rock Spire Isle Secret Cave",
      "Secret Cave Entrance on Shark Island": "Shark Island Secret Cave",
      "Secret Cave Entrance on Cliff Plateau Isles": "Cliff Plateau Isles Secret Cave",
      "Secret Cave Entrance on Horseshoe Island": "Horseshoe Island Secret Cave",
      "Secret Cave Entrance on Star Island": "Star Island Secret Cave",
      
      "Inner Entrance in Ice Ring Isle Secret Cave": "Ice Ring Isle Inner Cave",
      "Inner Entrance in Cliff Plateau Isles Secret Cave": "Cliff Plateau Isles Inner Cave",
      
      "Fairy Fountain Entrance on Outset Island": "Outset Fairy Fountain",
      "Fairy Fountain Entrance on Thorned Fairy Island": "Thorned Fairy Fountain",
      "Fairy Fountain Entrance on Eastern Fairy Island": "Eastern Fairy Fountain",
      "Fairy Fountain Entrance on Western Fairy Island": "Western Fairy Fountain",
      "Fairy Fountain Entrance on Southern Fairy Island": "Southern Fairy Fountain",
      "Fairy Fountain Entrance on Northern Fairy Island": "Northern Fairy Fountain",
    }
    
    self.done_entrances_to_exits: dict[ZoneEntrance, ZoneExit] = {}
    self.done_exits_to_entrances: dict[ZoneExit, ZoneEntrance] = {}
    self.nested_entrance_paths: list[list[str]] = []
    
    for entrance_name, exit_name in self.entrance_connections.items():
      zone_entrance = ZoneEntrance.all[entrance_name]
      zone_exit = ZoneExit.all[exit_name]
      self.done_entrances_to_exits[zone_entrance] = zone_exit
      self.done_exits_to_entrances[zone_exit] = zone_entrance

    self.entrances_plando = self.rando.plando.get("Entrances")
  
  def is_enabled(self) -> bool:
    return self.entrances_plando is not None
  
  @property
  def progress_randomize_duration_weight(self) -> int:
    return 5
  
  @property
  def progress_save_duration_weight(self) -> int:
    return 130
  
  @property
  def progress_randomize_text(self) -> str:
    return "Randomizing entrances..."
  
  @property
  def progress_save_text(self) -> str:
    return "Saving entrances..."
  
  def _randomize(self):
    entrances = DUNGEON_ENTRANCES + MINIBOSS_ENTRANCES + BOSS_ENTRANCES + SECRET_CAVE_ENTRANCES + SECRET_CAVE_INNER_ENTRANCES + FAIRY_FOUNTAIN_ENTRANCES
    exits = DUNGEON_EXITS + MINIBOSS_EXITS + BOSS_EXITS + SECRET_CAVE_EXITS + SECRET_CAVE_INNER_EXITS + FAIRY_FOUNTAIN_EXITS
    for zone_entrance in entrances:
      plando_exit = self.entrances_plando[zone_entrance.entrance_name]
      zone_exit = next(exit for exit in exits if exit.unique_name == plando_exit)
      self.entrance_connections[zone_entrance.entrance_name] = zone_exit.unique_name
      self.done_entrances_to_exits[zone_entrance] = zone_exit
      self.done_exits_to_entrances[zone_exit] = zone_entrance
    
    self.finalize_all_randomized_sets_of_entrances()
  
  def _save(self):
    self.update_all_entrance_destinations()
    self.update_all_boss_warp_out_destinations()
  
  def write_to_spoiler_log(self) -> str:
    spoiler_log = "Entrances:\n"
    for entrance_name, dungeon_or_cave_name in self.entrance_connections.items():
      spoiler_log += "  %-50s %s\n" % (entrance_name+":", dungeon_or_cave_name)
    
    def shorten_path_name(name):
      if name == "Dungeon Entrance on Dragon Roost Island":
        return "Dragon Roost Island (Main)"
      elif name == "Secret Cave Entrance on Dragon Roost Island":
        return "Dragon Roost Island (Pit)"
      elif re.search(r"^(Dungeon|Secret Cave|Inner) Entrance (on|in) ", name):
        _, short_name = re.split(r" (?:on|in) ", name, 1)
        return short_name
      elif match := re.search(r"^(Miniboss|Boss) Entrance in ", name):
        _, short_name = re.split(r" in ", name, 1)
        return f"{short_name} ({match.group(1)})"
      else:
        return name
    
    spoiler_log += "\n"
    
    spoiler_log += "Nested entrance paths:\n"
    for path in self.nested_entrance_paths:
      if len(path) < 3:
        # Don't include non-nested short paths (e.g. DRI -> Molgera).
        continue
      shortened_path = [shorten_path_name(name) for name in path[:-1]] + [path[-1]]
      spoiler_log += "  " + " -> ".join(shortened_path) + "\n"
    
    spoiler_log += "\n\n\n"
    return spoiler_log
  
  def finalize_all_randomized_sets_of_entrances(self):
    non_terminal_exits = []
    for en in ZoneEntrance.all.values():
      if en.nested_in is not None and en.nested_in not in non_terminal_exits:
        non_terminal_exits.append(en.nested_in)
    
    # Prepare some data so the spoiler log can display the nesting in terms of paths.
    self.nested_entrance_paths.clear()
    for zone_exit in ZoneExit.all.values():
      if zone_exit in non_terminal_exits:
        continue
      zone_entrance = self.done_exits_to_entrances[zone_exit]
      seen_entrances = self.get_all_entrances_on_path_to_entrance(zone_entrance)
      path = [zone_exit.unique_name]
      for entr in seen_entrances:
        path.append(entr.entrance_name)
      path.reverse()
      self.nested_entrance_paths.append(path)
    
    self.logic.update_entrance_connection_macros()
  #endregion
  
  
  #region Saving
  def update_all_entrance_destinations(self):
    for zone_exit, zone_entrance in self.done_exits_to_entrances.items():
      outermost_entrance = self.get_outermost_entrance_for_exit(zone_exit)
      self.update_entrance_to_lead_to_exit(zone_entrance, zone_exit, outermost_entrance)
  
  def update_all_boss_warp_out_destinations(self):
    for boss_exit in BOSS_EXITS:
      outermost_entrance = self.get_outermost_entrance_for_exit(boss_exit)
      assert outermost_entrance.warp_out_spawn_id is not None
      if boss_exit.unique_name == "Helmaroc King Boss Arena":
        # Special case, does not have a warp out event, just an exit.
        self.update_helmaroc_king_arena_ganon_door(boss_exit, outermost_entrance)
        continue
      self.update_boss_warp_out_destination(boss_exit.stage_name, outermost_entrance)
  
  def update_entrance_to_lead_to_exit(self, zone_entrance: ZoneEntrance, zone_exit: ZoneExit, outermost_entrance: ZoneEntrance):
    # Update the stage this entrance takes you into.
    entrance_dzr_path = "files/res/Stage/%s/Room%d.arc" % (zone_entrance.stage_name, zone_entrance.room_num)
    entrance_dzs_path = "files/res/Stage/%s/Stage.arc" % (zone_entrance.stage_name)
    entrance_dzr = self.rando.get_arc(entrance_dzr_path).get_file("room.dzr", DZx)
    entrance_dzs = self.rando.get_arc(entrance_dzs_path).get_file("stage.dzs", DZx)
    entrance_scls = entrance_dzr.entries_by_type(SCLS)[zone_entrance.scls_exit_index]
    entrance_scls.dest_stage_name = zone_exit.stage_name
    entrance_scls.room_index = zone_exit.room_num
    entrance_scls.spawn_id = zone_exit.spawn_id
    entrance_scls.save_changes()
    
    exit_dzr_path = "files/res/Stage/%s/Room%d.arc" % (zone_exit.stage_name, zone_exit.room_num)
    exit_dzs_path = "files/res/Stage/%s/Stage.arc" % zone_exit.stage_name
    exit_dzs = self.rando.get_arc(exit_dzs_path).get_file("stage.dzs", DZx)
    
    # Update the DRI spawn to not have spawn type 5.
    # If the DRI entrance was connected to the TotG dungeon, then exiting TotG while riding KoRL would crash the game.
    if len(entrance_dzs.entries_by_type(PLYR)) > 0:
      entrance_spawns = entrance_dzs.entries_by_type(PLYR)
    else:
      entrance_spawns = entrance_dzr.entries_by_type(PLYR)
    entrance_spawn = next(spawn for spawn in entrance_spawns if spawn.spawn_id == zone_entrance.spawn_id)
    if entrance_spawn.spawn_type == 5:
      entrance_spawn.spawn_type = 1
      entrance_spawn.save_changes()
    
    if zone_exit in MINIBOSS_EXITS + BOSS_EXITS:
      # Update the spawn you're placed at when saving and reloading inside a (mini)boss room.
      # For dungeons, the stage.dzs's SCLS exit at index 0 is always where to take you when saving
      # and reloading.
      exit_scls = exit_dzs.entries_by_type(SCLS)[0]
      if zone_entrance in MINIBOSS_ENTRANCES + BOSS_ENTRANCES:
        # If a dungeon's (mini)boss entrance connects to a (mini)boss, saving and reloading inside
        # the (mini)boss room should put you at the beginning of that dungeon, not the end.
        # But if multiple dungeons are nested we don't take the player all the way back to the
        # beginning of the chain, just to the beginning of the last dungeon.
        dungeon_start_exit = entrance_dzs.entries_by_type(SCLS)[0]
        exit_scls.dest_stage_name = dungeon_start_exit.dest_stage_name
        exit_scls.room_index = dungeon_start_exit.room_index
        exit_scls.spawn_id = dungeon_start_exit.spawn_id
        exit_scls.save_changes()
      else:
        # If an island entrance (or inner cave entrance) connects directly to a (mini)boss we put
        # you right outside that entrance.
        exit_scls.dest_stage_name = zone_entrance.stage_name
        exit_scls.room_index = zone_entrance.room_num
        exit_scls.spawn_id = zone_entrance.spawn_id
        exit_scls.save_changes()
    
    if zone_exit not in BOSS_EXITS:
      # Update the entrance you're put at when leaving the dungeon/secret cave/miniboss/inner cave.
      exit_dzr = self.rando.get_arc(exit_dzr_path).get_file("room.dzr", DZx)
      exit_scls = exit_dzr.entries_by_type(SCLS)[zone_exit.scls_exit_index]
      exit_scls.dest_stage_name = zone_entrance.stage_name
      exit_scls.room_index = zone_entrance.room_num
      exit_scls.spawn_id = zone_entrance.spawn_id
      exit_scls.save_changes()
    
    # Also update the extra exits when leaving Savage Labyrinth to put you on the correct entrance when leaving.
    if zone_exit.unique_name == "Savage Labyrinth":
      for stage_and_room_name in ["Cave10/Room0", "Cave10/Room20", "Cave11/Room0"]:
        savage_dzr_path = "files/res/Stage/%s.arc" % stage_and_room_name
        savage_dzr = self.rando.get_arc(savage_dzr_path).get_file("room.dzr", DZx)
        exit_sclses = [x for x in savage_dzr.entries_by_type(SCLS) if x.dest_stage_name == "sea"]
        for exit_scls in exit_sclses:
          exit_scls.dest_stage_name = zone_entrance.stage_name
          exit_scls.room_index = zone_entrance.room_num
          exit_scls.spawn_id = zone_entrance.spawn_id
          exit_scls.save_changes()
    
    if zone_exit in SECRET_CAVE_EXITS + FAIRY_FOUNTAIN_EXITS or zone_exit == ZoneExit.all["Ice Ring Isle Inner Cave"]:
      # Update the sector coordinates in the 2DMA chunk so that save-and-quitting in a cave puts you on the correct island.
      # This behavior applies to stages with stage ID 11-13 (checked at 80054B78 at dComIfGs_setGameStartStage).
      assert exit_dzs.entries_by_type(STAG)[0].stage_id in [11, 12, 13]
      _2dma = exit_dzs.entries_by_type(_2DMA)[0]
      island_number = self.rando.island_name_to_number[outermost_entrance.island_name]
      sector_x = (island_number-1) % 7
      sector_y = (island_number-1) // 7
      _2dma.sector_x = sector_x-3
      _2dma.sector_y = sector_y-3
      _2dma.save_changes()
    else:
      assert exit_dzs.entries_by_type(STAG)[0].stage_id not in [11, 12, 13]
    
    if zone_exit.unique_name == "Fire Mountain Secret Cave":
      actors = exit_dzr.entries_by_type(ACTR)
      kill_trigger = next(x for x in actors if x.name == "VolTag")
      if zone_entrance.entrance_name == "Secret Cave Entrance on Fire Mountain":
        # Unchanged from vanilla, do nothing.
        pass
      elif zone_entrance.entrance_name == "Secret Cave Entrance on Ice Ring Isle":
        # Ice Ring's entrance leads to Fire Mountain's exit.
        # Change the kill trigger on the inside of Fire Mountain to act like the one inside Ice Ring.
        kill_trigger.type = 2
        kill_trigger.save_changes()
      else:
        # An entrance without a timer leads into this cave.
        # Remove the kill trigger actor on the inside, because otherwise it would throw the player out the instant they enter.
        exit_dzr.remove_entity(kill_trigger, ACTR)
    
    if zone_exit.unique_name == "Ice Ring Isle Secret Cave":
      actors = exit_dzr.entries_by_type(ACTR)
      kill_trigger = next(x for x in actors if x.name == "VolTag")
      if zone_entrance.entrance_name == "Secret Cave Entrance on Ice Ring Isle":
        # Unchanged from vanilla, do nothing.
        pass
      elif zone_entrance.entrance_name == "Secret Cave Entrance on Fire Mountain":
        # Fire Mountain's entrance leads to Ice Ring's exit.
        # Change the kill trigger on the inside of Ice Ring to act like the one inside Fire Mountain.
        kill_trigger.type = 1
        kill_trigger.save_changes()
      else:
        # An entrance without a timer leads into this cave.
        # Remove the kill trigger actor on the inside, because otherwise it would throw the player out the instant they enter.
        exit_dzr.remove_entity(kill_trigger, ACTR)
  
  def update_boss_warp_out_destination(self, boss_stage_name, outermost_entrance: ZoneEntrance):
    # Update the wind warp out event to take you to the correct island.
    boss_stage_arc_path = "files/res/Stage/%s/Stage.arc" % boss_stage_name
    event_list = self.rando.get_arc(boss_stage_arc_path).get_file("event_list.dat", EventList)
    warp_out_event = event_list.events_by_name["WARP_WIND_AFTER"]
    director = next(actor for actor in warp_out_event.actors if actor.name == "DIRECTOR")
    stage_change_action = next(action for action in director.actions if action.name == "NEXT")
    stage_name_prop = next(prop for prop in stage_change_action.properties if prop.name == "Stage")
    stage_name_prop.value = outermost_entrance.warp_out_stage_name
    room_num_prop = next(prop for prop in stage_change_action.properties if prop.name == "RoomNo")
    room_num_prop.value = outermost_entrance.warp_out_room_num
    spawn_id_prop = next(prop for prop in stage_change_action.properties if prop.name == "StartCode")
    spawn_id_prop.value = outermost_entrance.warp_out_spawn_id
  
  def update_helmaroc_king_arena_ganon_door(self, hk_exit: ZoneExit, outermost_entrance: ZoneEntrance):
    # Update the door that originally lead into Ganondorf's room in vanilla.
    # In the randomizer, we use it in place of the WARP_WIND_AFTER warp out event.
    exit_dzr_path = "files/res/Stage/%s/Room%d.arc" % (hk_exit.stage_name, hk_exit.room_num)
    exit_dzr = self.rando.get_arc(exit_dzr_path).get_file("room.dzr", DZx)
    exit_scls = exit_dzr.entries_by_type(SCLS)[1]
    exit_scls.dest_stage_name = outermost_entrance.warp_out_stage_name
    exit_scls.room_index = outermost_entrance.warp_out_room_num
    exit_scls.spawn_id = outermost_entrance.warp_out_spawn_id
    exit_scls.save_changes()
  #endregion
  
  
  #region Convenience methods
  def get_all_entrance_sets_to_be_randomized(self):
    dungeons = True
    minibosses = True
    bosses = True
    secret_caves = True
    inner_caves = True
    fountains = True
    
    mix_entrances = EntranceMixMode.MIX_DUNGEONS
    any_dungeons = dungeons or minibosses or bosses
    any_non_dungeons = secret_caves or inner_caves or fountains
    
    if mix_entrances == EntranceMixMode.SEPARATE_DUNGEONS and any_dungeons and any_non_dungeons:
      yield self.get_one_entrance_set(dungeons=dungeons, minibosses=minibosses, bosses=bosses)
      yield self.get_one_entrance_set(caves=secret_caves, inner_caves=inner_caves, fountains=fountains)
    elif (any_dungeons or any_non_dungeons) and mix_entrances in [EntranceMixMode.SEPARATE_DUNGEONS, EntranceMixMode.MIX_DUNGEONS]:
      yield self.get_one_entrance_set(
        dungeons=dungeons, minibosses=minibosses, bosses=bosses,
        caves=secret_caves, inner_caves=inner_caves, fountains=fountains,
      )
    else:
      raise Exception("An invalid combination of entrance randomizer options was selected.")
  
  def get_one_entrance_set(self, *, dungeons=False, caves=False, minibosses=False, bosses=False, inner_caves=False, fountains=False):
    relevant_entrances: list[ZoneEntrance] = []
    relevant_exits: list[ZoneExit] = []
    if dungeons:
      relevant_entrances += DUNGEON_ENTRANCES
      relevant_exits += DUNGEON_EXITS
    if minibosses:
      relevant_entrances += MINIBOSS_ENTRANCES
      relevant_exits += MINIBOSS_EXITS
    if bosses:
      relevant_entrances += BOSS_ENTRANCES
      relevant_exits += BOSS_EXITS
    if caves:
      relevant_entrances += SECRET_CAVE_ENTRANCES
      relevant_exits += SECRET_CAVE_EXITS
    if inner_caves:
      relevant_entrances += SECRET_CAVE_INNER_ENTRANCES
      relevant_exits += SECRET_CAVE_INNER_EXITS
    if fountains:
      relevant_entrances += FAIRY_FOUNTAIN_ENTRANCES
      relevant_exits += FAIRY_FOUNTAIN_EXITS
    return relevant_entrances, relevant_exits
  
  def get_outermost_entrance_for_exit(self, zone_exit: ZoneExit):
    """ Unrecurses nested dungeons to determine what the outermost (island) entrance is for a given exit."""
    zone_entrance = self.done_exits_to_entrances[zone_exit]
    return self.get_outermost_entrance_for_entrance(zone_entrance)
  
  def get_outermost_entrance_for_entrance(self, zone_entrance: ZoneEntrance):
    """ Unrecurses nested dungeons to determine what the outermost (island) entrance is for a given entrance."""
    seen_entrances = self.get_all_entrances_on_path_to_entrance(zone_entrance)
    if seen_entrances is None:
      # Undecided.
      return None
    outermost_entrance = seen_entrances[-1]
    return outermost_entrance
  
  def get_all_entrances_on_path_to_entrance(self, zone_entrance: ZoneEntrance):
    """ Unrecurses nested dungeons to build a list of all entrances leading to a given entrance."""
    seen_entrances: list[ZoneEntrance] = []
    while zone_entrance.is_nested:
      if zone_entrance in seen_entrances:
        path_str = ", ".join([e.entrance_name for e in seen_entrances])
        raise Exception(f"Entrances are in an infinite loop: {path_str}")
      seen_entrances.append(zone_entrance)
      if zone_entrance.nested_in not in self.done_exits_to_entrances:
        # Undecided.
        return None
      zone_entrance = self.done_exits_to_entrances[zone_entrance.nested_in]
    seen_entrances.append(zone_entrance)
    return seen_entrances
  
  def is_item_location_behind_randomizable_entrance(self, location_name):
    loc_zone_name, _ = self.logic.split_location_name_by_zone(location_name)
    if loc_zone_name in ["Ganon's Tower", "Mailbox"]:
      # Ganon's Tower and the handful of Mailbox locations that depend on beating dungeon bosses are
      # considered to be "Dungeon" location types by the logic, but entrance randomizer does not
      # need to take them into account.
      # Although the mail locations are technically locked behind dungeons, we can still ignore them
      # here because if all of the locations in the dungeon itself are nonprogress, then any mail
      # depending on that dungeon should also be enforced as nonprogress by other parts of the code.
      return False
    
    types = self.logic.item_locations[location_name]["Types"]
    is_boss = "Boss" in types
    if loc_zone_name == "Forsaken Fortress" and not is_boss:
      # Special case. FF is a dungeon that is not randomized, except for the boss arena.
      return False
    
    is_big_octo = "Big Octo" in types
    if is_big_octo:
      # The Big Octo Great Fairy is the only Great Fairy location that is not also a Fairy Fountain.
      return False
    
    # In the general case we check if the location has a type corresponding to exits that can be
    # randomized.
    if any(t in ENTRANCE_RANDOMIZABLE_ITEM_LOCATION_TYPES for t in types):
      return True
      
    return False
  
  def get_entrance_zone_for_item_location(self, location_name: str) -> str:
    # Helper function to return the entrance zone name for the location.
    # For non-dungeon and non-cave locations, the entrance zone name is simply the zone/island name.
    # However, when entrances are randomized, the entrance zone name may differ from the zone name
    # for dungeons and caves.
    
    loc_zone_name, _ = self.logic.split_location_name_by_zone(location_name)
    
    if not self.is_item_location_behind_randomizable_entrance(location_name):
      return loc_zone_name
    
    zone_exit = self.item_location_name_to_zone_exit[location_name]
    assert zone_exit is not None, f"Could not determine entrance zone for item location: {location_name}"
    
    outermost_entrance = self.get_outermost_entrance_for_exit(zone_exit)
    return outermost_entrance.island_name
  
  def get_all_zones_for_item_location(self, location_name: str) -> list[str]:
    # Helper function to return a set of zone names that include the location.
    #
    # All returned zones are either an island name or a dungeon name - that is, if the entrance to
    # a cave is located on a different island, then the entrance island name is returned, but
    # the cave name is not.
    #
    # Locations in the Forsaken Fortress dungeon use "Forsaken Fortress" as the zone name, while
    # the Sunken Treasure location uses "Forsaken Fortress Sector".
    #
    # Boss and miniboss locations are considered part of their respective dungeons, even when those
    # entrances are randomized.
    #
    # A letter that is obtained from defeating a boss is considered part of the boss's dungeon.
    #
    # Here are some examples:
    # - If the location is inside Dragon Roost Cavern, which is inside Forbidden Woods, which is
    #   at the Outset Island cave entrance, then the returned value is {"Dragon Roost Cavern",
    #   "Forbidden Woods", "Outset Island"}.
    # - If the location is inside the Ice Ring Isle Cave, which is at the Private Oasis cave
    #   entrance, then the returned value is {"Private Oasis"}.
    # - If the location is the Helmaroc King Heart Container and Helmaroc King is at the Dragon
    #   Roost Island dungeon entrance, then the returned value is {"Forsaken Fortress",
    #   "Dragon Roost Island"}.
    # - If the location is inside the Star Island Cave, which is inside Wind Temple, which is at the
    #   Forsaken Fortress boss entrance, then the returned value is {"Wind Temple",
    #   "Forsaken Fortress"}.
    # - If the location is Letter from Baito and Jalhalla is at the Southern Fairy Island entrance,
    #   then the returned value is {"Mailbox", "Earth Temple", "Southern Fairy Island"}.
    
    loc_zone_name, _ = self.logic.split_location_name_by_zone(location_name)
    
    if location_name == "Mailbox - Letter from Baito":
      return {loc_zone_name} | self.get_all_zones_for_item_location("Earth Temple - Jalhalla Heart Container")
    if location_name == "Mailbox - Letter from Orca":
      return {loc_zone_name} | self.get_all_zones_for_item_location("Forbidden Woods - Kalle Demos Heart Container")
    if location_name == "Mailbox - Letter from Aryll" or location_name == "Mailbox - Letter from Tingle":
      return {loc_zone_name} | self.get_all_zones_for_item_location("Forsaken Fortress - Helmaroc King Heart Container")
    
    if not self.is_item_location_behind_randomizable_entrance(location_name):
      return {loc_zone_name}
    
    zone_exit = self.item_location_name_to_zone_exit[location_name]
    assert zone_exit is not None, f"Could not determine entrance zone for item location: {location_name}"
    
    zone_entrance = self.done_exits_to_entrances[zone_exit]
    entrances_on_path = self.get_all_entrances_on_path_to_entrance(zone_entrance)
    
    zones_for_item_location = set()
    
    for entrance in entrances_on_path:
      if entrance.island_name:
        zone_name = entrance.island_name
        # The Forsaken Fortress boss door is part of the dungeon, so we use "Forsaken Fortress" for
        # the zone name instead of "Forsaken Fortress Sector"
        if zone_name == "Forsaken Fortress Sector":
          zone_name = "Forsaken Fortress"

        zones_for_item_location.add(zone_name)
      elif entrance.nested_in in DUNGEON_EXITS:
        zones_for_item_location.add(entrance.nested_in.zone_name)
    
    if self.logic.is_dungeon_location(location_name):
      zones_for_item_location.add(loc_zone_name)
    
    return zones_for_item_location
  
  def get_zone_exit_for_item_location(self, location_name: str):
    if not self.is_item_location_behind_randomizable_entrance(location_name):
      return None
    
    zone_exit = ITEM_LOCATION_NAME_TO_EXIT_OVERRIDES.get(location_name, None)
    if zone_exit is not None:
      return zone_exit
    
    loc_zone_name, _ = self.logic.split_location_name_by_zone(location_name)
    possible_exits = [ex for ex in ZoneExit.all.values() if ex.zone_name == loc_zone_name]
    if len(possible_exits) == 0:
      return None
    elif len(possible_exits) == 1:
      return possible_exits[0]
    else:
      raise Exception(f"Multiple zone exits share the same zone name: {loc_zone_name!r}. Use a location exit override instead.")
  
  def get_entrance_zone_for_boss(self, boss_name: str) -> str:
    boss_arena_name = f"{boss_name} Boss Arena"
    zone_exit = ZoneExit.all[boss_arena_name]
    outermost_entrance = self.get_outermost_entrance_for_exit(zone_exit)
    return outermost_entrance.island_name
  #endregion
