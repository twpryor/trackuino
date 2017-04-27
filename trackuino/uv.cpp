// For use with ML8511


#include "config.h"
#include "uv.h"
#if (ARDUINO + 1) >= 100
#  include <Arduino.h>
#else
#  include <WProgram.h>
#endif
#include <stdlib.h>
#include <string.h>

void uv_setup()
{
    pinMode(UV_PIN, INPUT);
}

int uv_measure()
{
    int uv_read = 0;
    uv_read = analogRead(UV_PIN);
    return uv_read;
}
