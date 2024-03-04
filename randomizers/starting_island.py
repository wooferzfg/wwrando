
from randomizers.base_randomizer import BaseRandomizer
import tweaks

class StartingIslandRandomizer(BaseRandomizer):
  def __init__(self, rando):
    super().__init__(rando)
    
    # Default starting island (Outset Island) if the starting island randomizer is not on.
    self.room_number = 44
    self.starting_island_plando = self.rando.plando.get("Starting Island")
  
  def is_enabled(self) -> bool:
    return self.starting_island_plando is not None
  
  def _randomize(self):
    self.room_number = self.rando.island_name_to_number[self.starting_island_plando]
  
  def _save(self):
    tweaks.set_new_game_starting_spawn_id(self.rando, 0)
    tweaks.set_new_game_starting_room(self.rando, self.room_number)
    tweaks.change_ship_starting_island(self.rando, self.room_number)
  
  def write_to_spoiler_log(self) -> str:
    spoiler_log = "Starting island: "
    spoiler_log += self.rando.island_number_to_name[self.room_number]
    spoiler_log += "\n"
    
    spoiler_log += "\n\n\n"
    
    return spoiler_log
