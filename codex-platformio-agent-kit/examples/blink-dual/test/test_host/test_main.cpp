#include <cstring>
#include <unity.h>
#include "agent_blink.h"

void test_blink_interval_is_positive() {
    TEST_ASSERT_GREATER_THAN(0, blink_interval_ms());
}

void test_firmware_name_is_not_empty() {
    TEST_ASSERT_NOT_NULL(firmware_name());
    TEST_ASSERT_GREATER_THAN(0, strlen(firmware_name()));
}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    RUN_TEST(test_blink_interval_is_positive);
    RUN_TEST(test_firmware_name_is_not_empty);
    return UNITY_END();
}
