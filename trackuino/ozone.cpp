
#include "config.h"
#include "ozone.h"
#if (ARDUINO + 1) >= 100
#  include <Arduino.h>
#else
#  include <WProgram.h>
#endif
#include <stdlib.h>
#include <string.h>
    
int ozone_measure(){
    int input = analogRead(OZONE_PIN);
    return input;
}

