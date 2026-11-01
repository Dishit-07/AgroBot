#ifndef SOILSENSOR_H
#define SOILSENSOR_H

#include <Arduino.h>

struct SoilData {
    float moisture;      // %
    float soilTemp;      // °C
    float ph;            
    int nitrogen;        // mg/kg
    int phosphorus;      // mg/kg
    int potassium;       // mg/kg
    bool valid;
    unsigned long timestamp;
    String status;
};

void initSoilSensor(int rxPin, int txPin, int enPin);
bool readSoilSensor(SoilData &data);

#endif
