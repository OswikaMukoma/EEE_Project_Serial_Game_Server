# Hardware bring-up log

Append what you tried on the real board, with the exact result. Feeds the
validation and circuit-diagram sections. Save screenshots to docs/evidence/.

| Date | Who | What was tried | Result |
|---|---|---|---|
| | | | |

Paper checks (12 Oct, from the supplied PDFs, not yet bench-verified):
- STM32F051 datasheet DocID022265 Rev 4, Table 14, p.37: PA9 AF1 = USART1_TX, PA10 AF1 = USART1_RX.
- UCT dev board schematic v1.06 sheet 1: ST-Link VCP lines on PA9/PA10; SW0 PA0; R/G LED
  PB10 (via R12, red) and PB11 (via R13, green); D8 power LED.
