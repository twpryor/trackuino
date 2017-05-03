// For use with ML8511


#include "config.h"
#include "uv.h"
#if (ARDUINO + 1) >= 100
#  include <Arduino.h>
#else
#include <WProgram.h>
#endif
#include <stdlib.h>
#include <string.h>

void uv_setup()
{
    pinMode(UV_PIN, INPUT);
}

float uv_measure()
{
    int uvLevel = analogRead(UV_PIN);
    float uvIntensity = map(uvLevel, 0.99, 2.8, 0.0, 15.0); //Convert the voltage to a UV intensity level
    return uvIntensity;
}
