#include "config.h"
#include "uv.h"

int UVOUT_PIN = A8;
int REF_3V3_PIN = A9;

void UV_setup()
{
    pinMode(UVOUT_PIN, INPUT);
    pinMode(REF_3V3_PIN, INPUT);
}
float readUVSensor()
{
    int uvLevel = averageAnalogRead(UVOUT_PIN);
    int refLevel = averageAnalogRead(REF_3V3_PIN);
    
    // Use the 3.3V power pin as a reference to get a very accurate output value from sensor
    float outputVoltage = 3.3 / refLevel * uvLevel;

    float uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0); // Convert the voltage to a UV intensity level
    return uvIntensity;
}

int averageAnalogRead(int pinToRead)
{
    byte numberOfReadings = 8;
    unsigned int runningValue = 0; 

    for(int x = 0 ; x < numberOfReadings ; x++)
        runningValue += analogRead(pinToRead);
    runningValue /= numberOfReadings;

    return(runningValue);  
}

// The Arduino Map function but for floats
// From: http://forum.arduino.cc/index.php?topic=3922.0
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
