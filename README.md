# Serial Game Server

EEE3095S CS project 2026: an STM32F051 game server (authoritative) and a PC GUI
client (untrusted) talking over a serial link. Game: Tic-Tac-Toe (see
docs/decisions.md).

Status: Stage 0 (scaffold). See `docs/HANDOFF.md`.

## Build the firmware
Needs `arm-none-eabi-gcc` (or STM32CubeIDE's toolchain; the Makefile finds it).
```
make -C firmware
```
Output: `firmware/build/SerialGameServer.elf/.hex/.bin`. In STM32CubeIDE:
File > Import > C/C++ > Existing Code as Makefile Project, select `firmware/`.

## Layout
`docs/` protocol, plan, decisions, evidence, report - `firmware/` STM32 server -
`gui/` PC client - `tests/` pytest harness and mock server.

## Reused material
Firmware base (HAL/CMSIS drivers, startup, linker script, Makefile) adapted from
the EEE3096S Practical 2A starter project. AI assistance (Claude) used for
drafting; all code is reviewed and understood by both authors.
