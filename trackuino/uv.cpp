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

int uv_measure()
{
    int uvLevel = analogRead(UV_PIN);
    return uvLevel;
}

