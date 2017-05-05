

#ifndef UV_H
#define UV_H

void uv_setup();
float uv_measure();
int averageAnalogRead(int);
float mapfloat(float, float, float, float, float);

#define UV_PIN A2

#endif
