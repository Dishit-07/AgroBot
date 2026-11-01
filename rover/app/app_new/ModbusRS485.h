#ifndef MODBUS_RS485_H
#define MODBUS_RS485_H

#include <Arduino.h>

void modbusInit(int rxPin, int txPin, int enPin);
uint16_t modbusCRC(uint8_t *data, uint8_t length);
void sendModbusRequest(uint8_t slaveId, uint16_t startReg, uint16_t numRegs);
int readModbusResponse(uint8_t *buffer, uint8_t expectedBytes, unsigned long timeoutMs);

#endif
