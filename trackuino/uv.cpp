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
    pinMode(A5, INPUT);
}

int uv_measure()
{
    int uv_read = 0;
    uv_read = analogRead(A5);
    return uv_read;
}
