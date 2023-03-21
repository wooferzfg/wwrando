.org @NextFreeSpace
.global kill_link_on_crash
  kill_link_on_crash:
  stwu sp, -0x10 (sp)
  mflr r0
  stw r0, 0x14 (sp)

  andi. r0, r0, 0x0
  lis r6, gameInfo_mPlay_mCurrHP@ha
  addi r6, r6, gameInfo_mPlay_mCurrHP@l

  stw r0, 0x0 (r6)
  lis r5, -0x7fca

  lwz r0, 0x14 (sp)
  mtlr r0
  addi sp, sp, 0x10
  blr

.org 0x80115654
  bl kill_link_on_crash

.org @NextFreeSpace
.global kill_link_on_potion
  kill_link_on_potion:
  stwu sp, -0x10 (sp)
  mflr r0
  stw r0, 0x14 (sp)

  lis r3, -0x7FC4
  addi r3, r3, 0x4C08
  lfs f2, 0x5b5c (r3)
  lhz r0, 0x0 (r3)
  lfd f1, -0x5BC8 (r2)
  stw r0, 0xC (r1)
  lis r0, 0x4330
  stw r0, 0x8 (r1)
  lfd f0, 0x8 (r1)
  fsubs f0, f0, f1
  fadds f0, f2, f0
  fneg f0, f0
  stfs f0, 0x5b5c (r3)

  lwz r0, 0x14 (sp)
  mtlr r0
  addi sp, sp, 0x10
  blr

.org 0x80152390
  bl kill_link_on_potion
  nop
  nop
  nop
  nop
  nop
  nop
  nop
  nop
  nop
  nop

.org @NextFreeSpace
.global kill_link_on_ice
  kill_link_on_ice:
  stwu sp, -0x10 (sp)
  mflr r0
  stw r0, 0x14 (sp)

  andi. r0, r0, 0x0
  lis r28, gameInfo_mPlay_mCurrHP@ha
  addi r28, r28, gameInfo_mPlay_mCurrHP@l

  stw r0, 0x0 (r28)

  or r28, r4, r4

  lwz r0, 0x14 (sp)
  mtlr r0
  addi sp, sp, 0x10
  blr

.org 0x80119518
  bl kill_link_on_ice

.close