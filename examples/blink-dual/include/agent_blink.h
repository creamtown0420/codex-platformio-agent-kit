#pragma once

#ifndef BLINK_INTERVAL_MS
#define BLINK_INTERVAL_MS 500
#endif

inline int blink_interval_ms() {
    return BLINK_INTERVAL_MS;
}

inline const char* firmware_name() {
    return "codex-platformio-agent-kit blink";
}
