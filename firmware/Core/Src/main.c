/**
  * main.c - Serial Game Server, Stage 0 placeholder.
  *
  * Only proves that the project builds, flashes and runs: it blinks the green
  * status LED (PB11) at 1 Hz. Replace this in the firmware stages (see
  * docs/stages.md). Nothing here touches the UART, so the game link stays clean.
  */

#include "main.h"
#include "board.h"

void SystemClock_Config(void);

int main(void)
{
    HAL_Init();               /* starts SysTick at 1 ms (HAL_GetTick) */
    SystemClock_Config();

    RCC->AHBENR |= RCC_AHBENR_GPIOBEN;
    (void)RCC->AHBENR;        /* read-back: let the clock enable settle */

    /* PB10 and PB11 as push-pull outputs (MODER = 01). */
    LED_GREEN_GPIO->MODER = (LED_GREEN_GPIO->MODER
        & ~((3UL << (2u * LED_RED_PIN)) | (3UL << (2u * LED_GREEN_PIN))))
        | (1UL << (2u * LED_RED_PIN)) | (1UL << (2u * LED_GREEN_PIN));
    LED_RED_GPIO->BRR = (1UL << LED_RED_PIN);

    uint32_t last = 0u;
    while (1)
    {
        uint32_t now = HAL_GetTick();
        if ((uint32_t)(now - last) >= 500u)
        {
            last = now;
            LED_GREEN_GPIO->ODR ^= (1UL << LED_GREEN_PIN);
        }
    }
}

/** System clock: HSI, no PLL, AHB /1, APB /1 (8 MHz). Same as the course base. */
void SystemClock_Config(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    RCC_OscInitStruct.OscillatorType      = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState            = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
    RCC_OscInitStruct.PLL.PLLState        = RCC_PLL_NONE;
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
    {
        Error_Handler();
    }

    RCC_ClkInitStruct.ClockType      = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
                                     | RCC_CLOCKTYPE_PCLK1;
    RCC_ClkInitStruct.SYSCLKSource   = RCC_SYSCLKSOURCE_HSI;
    RCC_ClkInitStruct.AHBCLKDivider  = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
    {
        Error_Handler();
    }
}

void Error_Handler(void)
{
    __disable_irq();
    while (1)
    {
    }
}
