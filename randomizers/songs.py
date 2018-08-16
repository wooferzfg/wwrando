
import os
import re

from fs_helpers import *

def randomize_songs(self):
  offset = 3769844
  song_lengths = [3, 4, 4, 6, 6, 3]
  for i in range(6):
    num_notes = song_lengths[i]
    notes = []
    for j in range(6):
      if j < num_notes:
        cur_note = self.rng.choice([0, 1, 2, 3, 4])
        notes.append(cur_note)
      else:
        notes.append(255)
    if not self.dry_run:
      write_changed_song(self, offset, notes)
    offset += 7

def write_changed_song(self, offset, notes):
  path = os.path.join("sys", "main.dol")
  data = self.get_raw_file(path)
  for i in range(6):
    write_u8(data, offset + i + 1, notes[i])
