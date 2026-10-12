# HANDOFF (overwrite this file at the end of every turn)

Partners: A = <name>, B = <name>   |   Due: 25 Oct 2026 23:59   |   Today: 12 Oct

## Stage 1 draft done (2026-10-12), awaiting partner review
Built: docs/protocol.md v0.1 (framing, XOR checksum, 32-byte limit, 500 ms
timeout, all commands/errors, state table, validation order, invariants R1-R5);
docs/diagrams/ (fsm.dot, framer.dot, seq_game.mmd, seq_errors.mmd, rendered PNGs,
render.sh). Decisions D-009..D-012 recorded.
Verified: every example checksum recomputed by script (33 valid, 1 deliberately
wrong); the scripted win, the rejection sequence and the draw replayed against a
small reference model with the expected replies. Firmware not touched this stage.
Open:
- Both partners: read protocol.md, answer the six questions in section 12, then
  freeze (v1.0) and note it in decisions.md.
- Stage 4 (bring-up) can start now in parallel: confirm USART1 AF number in the
  datasheet, PC port name, baud; flash the placeholder and run the transmit/echo tests.
- GitHub repo not yet confirmed pushed; partner names still blank above.
- Project is ~4 days behind the 6 Oct plan: see "Revised schedule" in docs/stages.md.
Next: Stage 2 (game core, B) and Stage 3 (mock server + pytest, A) in parallel,
once the protocol is frozen. Stage 3 should implement docs/protocol.md exactly and
reuse the invariants R1-R5 as test names.

## Build and test
make -C firmware        (no tests yet; pytest harness arrives in Stage 3)
Re-render diagrams: docs/diagrams/render.sh   (needs dot, and mmdc for *.mmd)
