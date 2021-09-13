
import tweaks

def randomize_starting_island(self):
  starting_island_room_index = self.island_name_to_number[self.plando["Starting Island"]]
  
  if not self.dry_run:
    tweaks.set_new_game_starting_room_index(self, starting_island_room_index)
    tweaks.change_ship_starting_island(self, starting_island_room_index)
  
  self.starting_island_index = starting_island_room_index
