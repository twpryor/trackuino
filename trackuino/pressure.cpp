// For use with MPL3115A2


#include "config.h"
#include "pressure.h"
#if (ARDUINO + 1) >= 100
#include <Arduino.h>
#else
#include <WProgram.h>
#endif
#include <stdlib.h>
#include <string.h>
#include "SparkFunMPL3115A2.h"
#include <Wire.h>

float pressure_measure(){
    MPL3115A2 myPressure;
    Wire.begin();        // Join i2c bus
    myPressure.begin(); // Get sensor online
    // Configure the sensor
    //myPressure.setModeAltimeter(); // Measure altitude above sea level in meters
    myPressure.setModeBarometer(); // Measure pressure in Pascals from 20 to 110 kPa
    myPressure.setOversampleRate(7); // Set Oversample to the recommended 128
    myPressure.enableEventFlags(); // Enable all three pressure and temp event flags
    float pressure = myPressure.readPressure();
    /*while(100000 <= pressure) pressure /= 10;
    while(pressure < 10000) pressure *= 10;
    pressure = round(pressure);
    if(100000 <= pressure) pressure = round(pressure/10);*/
    return pressure;
}

