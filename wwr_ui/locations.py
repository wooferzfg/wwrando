from logic.logic import Logic

ITEM_LOCATIONS = list(Logic.load_and_parse_item_locations().keys())
ITEM_LOCATIONS.sort()

DEFAULT_EXCLUDED_LOCATIONS = []

DEFAULT_INCLUDED_LOCATIONS = ITEM_LOCATIONS.copy()
for item_name in DEFAULT_EXCLUDED_LOCATIONS:
  DEFAULT_INCLUDED_LOCATIONS.remove(item_name)
