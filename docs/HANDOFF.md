# HANDOFF (overwrite this file at the end of every turn)

Partners: A = <name>, B = <name>   |   Due: 25 Oct 2026 23:59   |   Today: 12 Oct

## Stages 1-3 done (12 Oct)
- Protocol v1.0 frozen (D-013).
- Stage 2: firmware/Core/Src/game.c + tests/core (50,546,417 checks, 0 failed);
  evidence docs/evidence/stage2_core_tests.txt; report draft docs/report/05_game_logic_draft.md.
- Stage 3: tests/ (mock_server.py, link.py, 100 pytest tests, all pass on the mock),
  15/15 injected faults caught (D-014). Evidence: docs/evidence/stage3_*.txt.
  tests/README.md explains commands.
Open / honest caveats:
- Second partner's own sign-off on protocol v1.0 is not recorded (D-013).
- Stage 1 explain-back (quiz) not done yet; each module must be explained by the
  driver and understood by the partner before it counts as done.
- An older tests/core/test_game.c was overwritten by a rewrite (covers more); check it.
- Unconfirmed on hardware: USART1 AF number, baud, SW0=PA0, R/G LED PB10/PB11.
- Rejected-move LED blink was only suggested; not in the spec.
- Plan PDF still shows the 6 Oct dates.
## Stage 4 (12 Oct): bring-up image READY, hardware steps NOT done
Claude cannot see or flash the board, so nothing below is verified on hardware yet.
Prepared: firmware/Core/Src/bringup.c, `make -C firmware BRINGUP=1`, tests/bringup_check.py,
UART_AF placeholder in board.h (D-015). Game build unchanged and still builds.
Bench steps for the partner with the board (record each result in docs/bringup-log.md):
1. Open the STM32F051C8 datasheet (DS8668) Table 14, rows PA9/PA10, read the AF number for
   USART1_TX/RX; add `#define UART_AF <n>u` to firmware/Core/Inc/board.h; note page/table.
2. `make -C firmware BRINGUP=1`, flash firmware/build/bringup/BringUp.bin (or .hex) with the
   usual tool; note the COM port name (Device Manager) in the log.
3. T1: after reset, 3 red then 3 green blinks? Write down which colour came first and whether
   it matches board.h (PB10 red, PB11 green).
4. Terminal (PuTTY etc., 115200 8N1) shows "BRINGUP TX n" each second. Screenshot -> docs/evidence/.
5. Close the terminal, run `python tests/bringup_check.py COMx`; paste output into the log.
6. Hold SW0: LED red and "SW0 DOWN"/"SW0 UP" in the terminal.
7. Circuit diagram (brief A.3) and a photo of the setup.
Then tell Claude the results; Stage 4 closes and Stage 5/6 firmware can start.
Remaining caveats from before still stand (partner sign-off on D-013, Stage 1 explain-back,
test_game.c rewrite, plan PDF dates, rejected-move LED idea).

## Build and test
make -C firmware ; make -C tests/core test ; pytest tests/ --port mock
Re-render diagrams: docs/diagrams/render.sh
