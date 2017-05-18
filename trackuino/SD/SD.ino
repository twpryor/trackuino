/*
  SD card read/write

 This example shows how to read and write data to and from an SD card file
 The circuit:
 * SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN)

 created   Nov 2010
 by David A. Mellis
 modified 9 Apr 2012
 by Tom Igoe
 modified 11 May 2017
 by Trevor Hedges

 This example code is in the public domain.

 */

#define UVPIN A0
#define OZONEPIN A1

#include <SPI.h>
#include <SD.h>

File myFile;
int cycle = 0;
int uv = 0;
int ozone = 0;
int currentFile = 0;
int prevFile = 0;
String filename;

void setup() {
    // Initialize SD
    SD.begin(4);

    // Write first file header
    filename = "data0.txt";
    writeHeader();
}

void loop() {
    
    // Serial.println(cycle);
    // Serial.println(cycle/300);

    readSensors();
    currentFile = cycle/300; // Every 300 seconds, save data to a new file, so that if any get corrupted, we only lose 5 min of data.
    filename = "data" + String(currentFile) + ".txt";

    // If 300 seconds have passed, write new file header
    if (currentFile != prevFile) {
        writeHeader();
    }
    
    writeData(currentFile);

    prevFile = currentFile;
    cycle += 1;
    delay(1000);
}

void readSensors() {
    uv = analogRead(UVPIN);
    ozone = analogRead(OZONEPIN);
}

void writeHeader(){
    myFile = SD.open(filename, FILE_WRITE);
    myFile.println("Time after power on (ms), UV, Ozone");
    myFile.close();
}

void writeData(int filecount) {
    // Define filename
    myFile = SD.open(filename, FILE_WRITE);
    
    myFile.println(String(millis()) + "," + String(uv) + "," + String(ozone));

    // Close file
    myFile.close();
}


