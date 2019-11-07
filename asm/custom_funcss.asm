
.open "sys/main.dol"
.org 0x803FCFA8

.global init_save_with_tweaks
init_save_with_tweaks:
; Function start stuff
stwu sp, -0x10 (sp)
mflr r0
stw r0, 0x14 (sp)


bl init__10dSv_save_cFv ; To call this custom func we overwrote a call to init__10dSv_save_cFv, so call that now.

; Give user-selected custom starting items
bl init_starting_gear

lis r3, 0x803C5D60@ha
addi r3, r3, 0x803C5D60@l
li r4, 0x0310 ; Saw event where Grandma gives you the Hero's Clothes
bl onEventBit__11dSv_event_cFUs

lis r5, should_start_with_heros_clothes@ha
addi r5, r5, should_start_with_heros_clothes@l
lbz r5, 0 (r5) ; Load bool of whether player should start with Hero's clothes
cmpwi r5, 1
bne after_starting_heros_clothes
lis r3, 0x803C522C@ha
addi r3, r3, 0x803C522C@l
li r4, 0x2A80 ; HAS_HEROS_CLOTHES
bl onEventBit__11dSv_event_cFUs
after_starting_heros_clothes:

; Function end stuff
lwz r0, 0x14 (sp)
mtlr r0
addi sp, sp, 0x10
blr


; This function reads from an array of user-selected starting item IDs and adds them to your inventory.
.global init_starting_gear
init_starting_gear:
stwu sp, -0x10 (sp)
mflr r0
stw r0, 0x14 (sp)
stw r31, 0xC (sp)

lis r31, starting_gear@ha
addi r31, r31, starting_gear@l
lbz r3, 0 (r31)
b init_starting_gear_check_continue_loop

init_starting_gear_begin_loop:
bl convert_progressive_item_id
; bl execItemGet__FUc
lbzu r3, 1(r31)
init_starting_gear_check_continue_loop:
cmplwi r3, 255
bne+ init_starting_gear_begin_loop

end_init_starting_gear:
lwz r31, 0xC (sp)
lwz r0, 0x14 (sp)
mtlr r0
addi sp, sp, 0x10
blr


.global should_start_with_heros_clothes
should_start_with_heros_clothes:
.byte 1 ; By default start with the Hero's Clothes
.global sword_mode
sword_mode:
.byte 0 ; By default Start with Sword
.global skip_rematch_bosses
skip_rematch_bosses:
.byte 1 ; By default skip them

.global starting_gear
starting_gear:
.space 47, 0xFF ; Allocate space for up to 47 additional items (when changing this also update the constant in tweaks.py)
.byte 0xFF

.align 2 ; Align to the next 4 bytes

; Updates the current wind direction to match KoRL's direction.
.global set_wind_dir_to_ship_dir
set_wind_dir_to_ship_dir:
stwu sp, -0x10 (sp)
mflr r0
stw r0, 0x14 (sp)

; First call setShipSailState since we overwrote a call to this in KoRL's code in order to call this custom function.
bl setShipSailState__11JAIZelBasicFl

lis r3,0x803CA75C@ha
addi r3,r3,0x803CA75C@l
lwz r3, 0 (r3) ; Read the pointer to KoRL's entity
lha r3, 0x206 (r3) ; Read KoRL's Y rotation
neg r3, r3 ; Negate his Y rotation since it's backwards
addi r4, r3, 0x4000 ; Add 90 degrees to get the diretion KoRL is actually facing
addi r4, r4, 0x1000 ; Add another 22.5 degrees in order to help round to the closest 45 degrees.
rlwinm r4,r4,0,0,18 ; Now AND with 0xFFFFE000 in order to round down to the nearest 0x2000 (45 degrees). Because we added 22.5 degrees first, this accomplishes rounding either up or down to the nearest 45 degrees, whichever is closer.

li r3, 0
bl dKyw_tact_wind_set__Fss ; Pass the new angle as argument r4 to the function that changes wind direction

lwz r0, 0x14 (sp)
mtlr r0
addi sp, sp, 0x10
blr


.global slow_down_ship_when_stopping
slow_down_ship_when_stopping:
stwu sp, -0x10 (sp)
mflr r0
stw r0, 0x14 (sp)

lis r4, ship_stopping_deceleration@ha
addi r4, r4, ship_stopping_deceleration@l
lfs f3, 0 (r4) ; Max deceleration per frame
lfs f4, 4 (r4) ; Min deceleration per frame

bl cLib_addCalc__FPfffff

lwz r0, 0x14 (sp)
mtlr r0
addi sp, sp, 0x10
blr

ship_stopping_deceleration:
.float 2.0 ; Max deceleration, 1.0 in vanilla
.float 0.2 ; Min deceleration, 0.1 in vanilla


.global check_run_new_text_commands

.global exec_curr_num_keys_text_command


.global slow_down_ship_when_idle
slow_down_ship_when_idle:
stwu sp, -0x10 (sp)
mflr r0
stw r0, 0x14 (sp)

lis r4, ship_idle_deceleration@ha
addi r4, r4, ship_idle_deceleration@l
lfs f3, 0 (r4) ; Max deceleration per frame
lfs f4, 4 (r4) ; Min deceleration per frame

bl cLib_addCalc__FPfffff

lwz r0, 0x14 (sp)
mtlr r0
addi sp, sp, 0x10
blr

ship_idle_deceleration:
.float 2.0 ; Max deceleration, 1.0 in vanilla
.float 0.1 ; Min deceleration, 0.05 in vanilla








; Borrows logic used for vanilla rope hang turning and injects some of the rotation logic into the rope swinging function.
; The main difference between the way the vanilla rope hanging function turns the player and this custom function is that the vanilla function uses a maximum rotational velocity per frame of 0x200, and a rotational acceleration of 0x40.
; But 0x200 units of rotation per frame would be far too fast to control when the player is swinging, and they could clip through walls very easily.
; So instead we just use the rotational acceleration as a constant rotational velocity instead, with no acceleration or deceleration.
.global turn_while_swinging
turn_while_swinging:

lis r3, 0x803A4DF0@ha
addi r3, r3, 0x803A4DF0@l
lfs f0, 0 (r3) ; Control stick horizontal axis (from -1.0 to 1.0)
lfs f1, -0x5A18 (r2) ; Load the float constant at 803FA2E8 for the base amount of rotational velocity to use (vanilla value is 0x40, this constant is originally used as rotational acceleration by the rope hanging function)
fmuls f0, f1, f0 ; Get the current amount of rotational velocity to use this frame after adjusting for the control stick amount

; Convert current rotational velocity to an integer.
; (sp+0x68 was used earlier on in procRopeSwing__9daPy_lk_cFv for float conversion so we just reuse this same space.)
fctiwz  f0, f0
stfd f0, 0x68 (sp)
lwz r0, 0x6C (sp)

; Convert base rotational velocity to an integer.
fctiwz  f1, f1
stfd f1, 0x68 (sp)
lwz r3, 0x6C (sp)

; If the player isn't moving the control stick horizontally very much (less than 25%), don't turn the player at all.
rlwinm r3, r3, 30, 2, 31 ; Divide the base rotational velocity by 4 to figure out what the threshold should be for 25% on the control stick.
cmpw r0, r3
bge turn_while_swinging_update_angle ; Control stick is >=25%
neg r3, r3
cmpw r0, r3
ble turn_while_swinging_update_angle ; Control stick is <=-25%
b turn_while_swinging_return

turn_while_swinging_update_angle:
; Subtract rotational velocity from the player's rotation. (Both player_entity+20E and +206 have the player's rotation.)
lha r3, 0x020E (r31)
sub r0, r3, r0
sth r0, 0x020E (r31)
sth r0, 0x0206 (r31)

turn_while_swinging_return:
lfs f0, -0x5BA8 (rtoc) ; Replace line we overwrote to branch here
b 0x8014564C ; Return







; Check the ID of the upcoming text command to see if it's a custom one, and runs custom code for it if so.
.global check_run_new_text_commands
check_run_new_text_commands:
clrlwi. r6,r0,24
bne check_run_new_text_commands_check_failed

lbz r6,3(r3)
cmplwi r6,0
bne check_run_new_text_commands_check_failed

lbz r6,4(r3)
cmplwi r6, 0x4B ; Lowest key counter text command ID
blt check_run_new_text_commands_check_failed
cmplwi r6, 0x4F ; Highest key counter text command ID
bgt check_run_new_text_commands_check_failed

mr r3,r31
mr r4, r6
bl exec_curr_num_keys_text_command
b 0x80034D34 ; Return (to after a text command has been successfully executed)


check_run_new_text_commands_check_failed:
clrlwi r0,r0,24 ; Replace the line we overwrote to jump here
b 0x80033E78 ; Return (to back inside the code to check what text command should be run)







; Manually animate rainbow rupees to cycle through all other rupee colors.
; In order to avoid an abrupt change from silver to green when it loops, we make the animation play forward and then backwards before looping, so it's always a smooth transition.
.global check_animate_rainbow_rupee_color
check_animate_rainbow_rupee_color:

; Check if the color for this rupee specified in the item resources is 7 (originally unused, we use it as a marker to separate the rainbow rupee from other color rupees).
cmpwi r0, 7
beq animate_rainbow_rupee_color

; If it's not the rainbow rupee, replace the line of code we overwrote to jump here, and then return to the regular code for normal rupees.
lfd f1, -0x5DF0 (rtoc)
b 0x800F93F8

animate_rainbow_rupee_color:

; If it is the rainbow rupee, we need to increment the current keyframe (a float) by certain value every frame.
; (Note: The way this is coded would increase it by this value multiplied by the number of rainbow rupees being drawn. This is fine since there's only one rainbow rupee but would cause issues if we placed multiple of them. Would need to find a different place to increment the keyframe in that case, somewhere only called once per frame.)
lis r5, rainbow_rupee_keyframe@ha
addi r5, r5, rainbow_rupee_keyframe@l
lfs f1, 0 (r5) ; Read current keyframe
lfs f0, 4 (r5) ; Read amount to add to keyframe per frame
fadds f1, f1, f0 ; Increase the keyframe value

lfs f0, 8 (r5) ; Read the maximum keyframe value
fcmpo cr0,f1,f0
; If we're less than the max we don't need to reset the value
blt store_rainbow_rupee_keyframe_value

; If we're greater than the max, reset the current keyframe to the minimum.
; The minimum is actually the maximum negated. This is to signify that we're playing the animation backwards.
lfs f1, 0xC (r5)

store_rainbow_rupee_keyframe_value:
stfs f1, 0 (r5) ; Store the new keyframe value back

; Take the absolute value of the keyframe. So instead of going from -6 to +6, the value we pass as the actual keyframe goes from 6 to 0 to 6.
fabs f1, f1

b 0x800F9410

.global rainbow_rupee_keyframe
rainbow_rupee_keyframe:
.float 0.0 ; Current keyframe, acts as a global variable modified every frame
.float 0.15 ; Amount to increment keyframe by every frame a rainbow rupee is being drawn
.float 6.0 ; Max keyframe, when it should loop
.float -6.0 ; Minimum keyframe


.close