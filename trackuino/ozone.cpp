
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
    
}
