// For use with MPL3115A2


#include "config.h"
#include "pressure.h"
#if (ARDUINO + 1) >= 100
#  include <Arduino.h>
#else
#include <WProgram.h>
#endif
#include <stdlib.h>
#include <string.h>
#include <Wire.h>

void pressure_setup()
{
    pinMode(A5, INPUT);
}

int pressure_measure()
{
    int pressure_read = 0;
    uv_read = analogRead(A5);
    return uv_read;
}

