
#include "config.h"
#include "ozone.h"
#if (ARDUINO + 1) >= 100
#  include <Arduino.h>
#else
#  include <WProgram.h>
#endif
#include <stdlib.h>
#include <string.h>

void ozone_setup(){
    pinMode(OZONE_PIN, INPUT);
}
    
int ozone_measure(){
    int input = analogRead(OZONE_PIN);
    return mapfloat(input, 0.0, 1024.0, 0.0, 5.0); // Map analog output to a voltage reading for later use
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
