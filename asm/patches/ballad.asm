; Modify the code for warping with the Ballad of Gales to get rid of the cutscene that accompanies it.
.open "files/rels/d_a_ship.rel"
.org 0x7A10
  ; Get rid of the line that checks if KoRL has reached a high enough Y pos to start the warp yet.
  nop
.org 0x7680
  ; Get rid of the line that plays the warping music, since it would continue playing after the warp has happened.
  nop
.close