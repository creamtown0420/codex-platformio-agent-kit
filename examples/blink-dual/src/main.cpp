#include "agent_blink.h"

#if defined(ARDUINO)
#include <Arduino.h>

#ifndef LED_PIN
#if defined(LED_BUILTIN)
#define LED_PIN LED_BUILTIN
#else
#define LED_PIN 2
#endif
#endif

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    Serial.println(firmware_name());
    Serial.print("blink_interval_ms=");
    Serial.println(blink_interval_ms());
}

void loop() {
    digitalWrite(LED_PIN, HIGH);
    delay(blink_interval_ms());
    digitalWrite(LED_PIN, LOW);
    delay(blink_interval_ms());
}

#else
#include <iostream>

int main() {
    std::cout << firmware_name() << "\n";
    std::cout << "blink_interval_ms=" << blink_interval_ms() << "\n";
    return blink_interval_ms() > 0 ? 0 : 1;
}
#endif
