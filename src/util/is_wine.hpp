#pragma once
#include "memory/module.hpp"

#include "env.hpp"

namespace big
{
    inline bool is_wine()
    {
        static auto module = memory::module("ntdll.dll");
        
        // Wine's ntdll exports this function: https://wiki.winehq.org/Developer_FAQ#How_can_I_detect_Wine?
        return module.get_export("wine_get_version").operator bool();
    }

    inline bool is_proton()
    {
        // Proton wouldn't start without this environment variable: https://github.com/ValveSoftware/Proton/blob/bc4d2acf3ba8c3edd8ba915e520996ed811eaf3c/proton#L1496C13-L1496C35
        static const auto steam_compatible = env::get("STEAM_COMPAT_DATA_PATH");
        
        return is_wine() && steam_compatible;
    }
}
