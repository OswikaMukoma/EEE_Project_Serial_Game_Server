/**
  * board.h - UCT Dev Board (STM32F051C8) facts used by the game server.
  *
  * Source: Board.md in the course repo (KiCad v1.06). Pins below are what that
  * document says; confirm each one on the real board before relying on it and
  * note the result in docs/bringup-log.md.
  *
  * UART: USART1 on PA9 (TX) and PA10 (RX), wired to the on-board ST-Link
  * virtual COM port (decision D-008). No adapter board.
  */
#ifndef BOARD_H
#define BOARD_H

#include "stm32f0xx.h"

/* Status LED (red/green package) on port B, 150 ohm series resistors. */
#define LED_RED_GPIO     GPIOB
#define LED_RED_PIN      10u
#define LED_GREEN_GPIO   GPIOB
#define LED_GREEN_PIN    11u

/* Tactile push-buttons SW0..SW3 on PA0..PA3, pull to GND when pressed
 * (active low; enable the internal pull-up). */
#define BTN_GPIO         GPIOA
#define BTN_SW0_PIN      0u

/* Game UART = USART1 via the ST-Link virtual COM port (D-008).
 * UART_AF: alternate-function number that routes USART1_TX/RX to PA9/PA10.
 * NOT FILLED IN ON PURPOSE: read it from the STM32F051x8 datasheet, Table 14
 * "Alternate functions selected through GPIOA_AFR registers for port A"
 * (PA9 = USART1_TX, PA10 = USART1_RX per Table 13), then define it below as
 * a number, e.g. "#define UART_AF 7u" (7 is only an example format, NOT a value).
 * Record the page/table in docs/bringup-log.md. The bring-up build stops with
 * an #error until this is set. */
/* #define UART_AF   <number from Table 14> */
#define UART_GPIO        GPIOA
#define UART_TX_PIN      9u
#define UART_RX_PIN      10u

#endif /* BOARD_H */
