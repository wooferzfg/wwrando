
;Remove song replays, where Link plays a fancy animation to conduct the song after the player plays it.
.open "sys/main.dol"
.org 0x8014ECE0
  ; Originally checked if the "You conducted..." text box has disappeared.
  ; Remove that check.
  nop
.org 0x8014EF28
  ; Originally checked if Link's conducting animation has finished playing.
  ; Remove that check.
  nop
.close
