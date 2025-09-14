#include <cstdio>
#include <cstdint>

struct ServerInfo {
    // Assuming `handle` is a pointer to an `InterfaceController` instance.
    void* handle;
};

class LocaleGuard {
public:
    LocaleGuard() {
        // Constructor saves the current locale and sets the desired one.
    }

    ~LocaleGuard() {
        // Destructor restores the original locale.
    }
};

class InterfaceController {
public:
    void updateState(const char* stateName, const char* stateValue) {
        // Implementation to update the state of the interface.
    }
};


void transmitAdjustmentToServer(ServerInfo* const server, int64_t unitId, int settingId, float newValue)
{
    char settingBuffer[20] = {};
    {
        const LocaleGuard localeGuard;
        std::snprintf(settingBuffer, sizeof(settingBuffer), "%lld:%d:%f", (long long)unitId, settingId, newValue);
    }
    static_cast<InterfaceController*>(server->handle)->updateState("adjustment", settingBuffer);
}