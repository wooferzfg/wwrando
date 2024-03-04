
import os

from wwrando_paths import RANDO_ROOT_PATH

with open(os.path.join(RANDO_ROOT_PATH, "plando_version.txt"), "r") as f:
  PLANDO_VERSION = f.read().strip()
with open(os.path.join(RANDO_ROOT_PATH, "version.txt"), "r") as f:
  VERSION = f.read().strip()

VERSION_WITHOUT_COMMIT = VERSION
