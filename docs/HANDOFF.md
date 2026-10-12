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
Next: Stage 4 bring-up on the board (B) then Stages 5+6 firmware framer/FSM using the
tests unchanged: `pytest tests/ --port COMx`. GUI (Stage 8) can start now against
`python tests/mock_server.py --listen 5555` (socket://127.0.0.1:5555).

## Build and test
make -C firmware ; make -C tests/core test ; pytest tests/ --port mock
Re-render diagrams: docs/diagrams/render.sh
