
from collections import OrderedDict

OPTIONS = OrderedDict([
  (
    "custom_player_model",
    "Replaces Link's model with a custom player model.\nThese are loaded from the /models folder."
  ),
  (
    "player_in_casual_clothes",
    "Enable this if you want to wear your casual clothes instead of the Hero's Clothes."
  ),
  (
    "disable_custom_player_voice",
    "If the chosen custom model comes with custom voice files, you can check this option to turn them off and simply use Link's normal voice instead."
  ),
  (
    "instant_text_boxes",
    "Text appears instantly.<br>Also, the B button is changed to instantly skip through text as long as you hold it down."
  ),
  (
    "swift_sail",
    "Sailing speed is doubled and the direction of the wind is always at your back as long as the sail is out."
  ),
  (
    "increase_player_movement_speeds",
    "Change rolling so that it scales from 20.0 to 26.0 speed depending on the player's speed when they roll."
  ),
  (
    "increase_grapple_animation_speed",
    "Speeds up the grappling hook significantly to behave similarly to HD."
  ),
  (
    "increase_block_moving_animation",
    "Speeds up the rate in which blocks move when pushed/pulled."
  ),
  (
    "increase_misc_animations",
    "Speeds up crawling, climbing, and the camera zoom when talking to an npc."
  ),
  (
    "tingle_chests_without_tuner",
    "Allows Tingle chests to be found with normal bombs, compass reveals location."
  ),
  (
    "invert_camera_x_axis",
    "Changes camera to control like it does in HD."
  ),
  (
    "reveal_full_sea_chart",
    "Reveals the whole sea chart during file creation, does not apply to existing saves."
  ),
])

NON_PERMALINK_OPTIONS = [
  "custom_player_model",
  "invert_camera_x_axis",
  "player_in_casual_clothes",
  "disable_custom_player_voice",
]
