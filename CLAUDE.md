# CLAUDE.md - Serial Game Server (EEE3095S CS project 2026)

Two-student project. An STM32F051 (UCT dev board) is the **authoritative game
server**; a PC GUI is a thin, **untrusted** client. Due **25 Oct 2026, 23:59**
(late penalty 10%/day). Marks reward sound embedded software, a robust protocol,
rule enforcement and repeatable tests, so correctness and evidence beat game
complexity.

## Start of every session
1. Read `docs/HANDOFF.md` (where we are, what is next) and `docs/stages.md`.
2. Summarise the state back to the user so stale information gets caught.
3. Do only the current stage. At the end, update HANDOFF/decisions/evidence (below).

## Source of truth
- `docs/protocol.md` is the single source of truth for framing, commands and
  errors. **Never change behaviour without asking, and update protocol.md in the
  same commit as the code.**
- `docs/decisions.md` is append-only: log every non-trivial choice and why.

## Game and rules
- Game: Tic-Tac-Toe (3x3, board string of 9 chars: `.` empty, `X`, `O`).
  Stretch, in order: server-side AI, hardware-timer move clock, move undo.
- Server states: IDLE, IN_PROGRESS, GAME_OVER. IDLE accepts CONNECT/NEW;
  IN_PROGRESS accepts MOVE/STATE/RESIGN; GAME_OVER accepts NEW/STATE/DISCONNECT.
- **Validate-then-commit:** check state, turn, range and occupancy first; modify
  the board only after every check passes. A rejected request must never change
  any state (the report must argue this).
- Specific NACKs: `NACK:OCCUPIED`, `NACK:RANGE`, `NACK:NOTURN`, `NACK:NOGAME`,
  `NACK:BADCMD` (plus any we document, e.g. bad checksum).
- GUI redraws only from a valid server response, never optimistically.

## Firmware rules (STM32F051C8: 64 KB flash, 8 KB RAM, Cortex-M0)
- Game logic (`game.c/.h`) is portable C with **no HAL/CMSIS calls**, so it can
  be compiled and unit-tested on the PC.
- UART: RX interrupt -> ring buffer -> line framer in the main loop. Newline
  terminator, max frame length (decide in protocol.md), partial-frame timeout
  via SysTick, oversize/garbage -> `NACK:BADCMD`. **Never block in the parser.**
- **Nothing else may be written to the game UART** (no debug prints; use a
  compile flag if debug output is ever needed). It would corrupt the protocol
  and the tests.
- Hardware behaviour: on-board button (new game / reset) and LED (turn / game
  over) - required by the brief.
- UART = USART1, PA9 (TX) / PA10 (RX), through the on-board ST-Link virtual COM
  port (decision D-008). No adapter board is used. Other pin facts come from
  `Board.md` in the course repo and must be confirmed on the bench. Do not guess
  register fields, alternate functions or pins.

## Layout
```
docs/       protocol.md, stages.md, HANDOFF.md, decisions.md, bringup-log.md,
            evidence/ (test output, serial captures, screenshots), report/
firmware/   STM32 project (Makefile build; imports into STM32CubeIDE as a
            Makefile project). Core/Src, Core/Inc, Drivers (do not edit).
gui/        PC client (Python; library TBD in decisions.md)
tests/      pytest harness + mock server; serial port via --port or env var
```

## Commands
```
make -C firmware            # build -> firmware/build/SerialGameServer.elf
make -C firmware clean
make -C tests/core test     # game core unit tests on the PC
pytest tests/ --port mock   # mock server, no board (~2 min; -m "not slow" skips timeouts)
python tests/mutation_check.py   # inject faults into the mock; all must be caught
pytest tests/ --port COMx   # real board; close any terminal using that port
```
Toolchain: `arm-none-eabi-gcc` (apt: `gcc-arm-none-eabi libnewlib-arm-none-eabi`).

## Working agreement
- Small tasks, small commits. Run builds/tests and show the output; never
  report "tests pass" without running them.
- Every module must be explained back by the driver and understood by the
  partner before the stage counts as done (demo and report marks depend on it).
- The navigator proposes nasty cases (garbage, wrong state, off-by-one); each
  becomes a test.
- Keep evidence as we go in `docs/evidence/`; draft each report section while
  the work is fresh in `docs/report/`.
- This repo is separate from the course lab repo. Never commit project work there.
- AI assistance is allowed; disclose it and the reused course base in the report
  references.
