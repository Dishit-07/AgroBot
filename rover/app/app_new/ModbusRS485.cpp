#include "ModbusRS485.h"
#include <HardwareSerial.h>

extern HardwareSerial RS485Serial;
static int _enPin = -1;
extern bool debugModbus;

void modbusInit(int rxPin, int txPin, int enPin) {
    _enPin = enPin;
    pinMode(_enPin, OUTPUT);
    digitalWrite(_enPin, LOW); // Receive mode by default
    RS485Serial.begin(4800, SERIAL_8N1, rxPin, txPin);
}

uint16_t modbusCRC(uint8_t *data, uint8_t length) {
    uint16_t crc = 0xFFFF;
    for (int pos = 0; pos < length; pos++) {
        crc ^= (uint16_t)data[pos];
        for (int i = 8; i != 0; i--) {
            if ((crc & 0x0001) != 0) {
                crc >>= 1;
                crc ^= 0xA001;
            } else {
                crc >>= 1;
            }
        }
    }
    return crc;
}

void sendModbusRequest(uint8_t slaveId, uint16_t startReg, uint16_t numRegs) {
    uint8_t request[8];
    request[0] = slaveId;
    request[1] = 0x03; // Read Holding Registers
    request[2] = startReg >> 8;
    request[3] = startReg & 0xFF;
    request[4] = numRegs >> 8;
    request[5] = numRegs & 0xFF;
    
    uint16_t crc = modbusCRC(request, 6);
    request[6] = crc & 0xFF; // Low byte first
    request[7] = crc >> 8;
    
    if (debugModbus) {
        Serial.print("[MODBUS] TX: ");
        for (int i = 0; i < 8; i++) {
            if (request[i] < 0x10) Serial.print("0");
            Serial.print(request[i], HEX);
            Serial.print(" ");
        }
        Serial.println();
    }
    
    // Clear any pending incoming bytes
    while(RS485Serial.available()) RS485Serial.read();
    
    digitalWrite(_enPin, HIGH); // Transmit mode
    RS485Serial.write(request, 8);
    RS485Serial.flush(); // Wait for transmission to complete
    digitalWrite(_enPin, LOW); // Receive mode
}

int readModbusResponse(uint8_t *buffer, uint8_t expectedBytes, unsigned long timeoutMs) {
    unsigned long start = millis();
    int count = 0;
    while (millis() - start < timeoutMs) {
        if (RS485Serial.available()) {
            buffer[count++] = RS485Serial.read();
            if (count >= expectedBytes) break;
        }
    }
    
    if (debugModbus && count > 0) {
        Serial.print("[MODBUS] RX: ");
        for (int i = 0; i < count; i++) {
            if (buffer[i] < 0x10) Serial.print("0");
            Serial.print(buffer[i], HEX);
            Serial.print(" ");
        }
        Serial.println();
    }
    
    return count;
}
