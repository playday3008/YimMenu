#ifndef COMMON_INC
#define COMMON_INC

// clang-format off

#define __STDC_WANT_LIB_EXT1__ 1

#include <sdkddkver.h>
#include <winsock2.h>
#include <windows.h>
#include <d3d11.h>

#include <cinttypes>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <cstring>

#if !defined(__STDC_LIB_EXT1__) && (defined(_MSC_VER) && __STDC_WANT_SECURE_LIB__ != 1)
#define strcpy_s(dest, destsz, src) strcpy(dest, src)
#define strncpy_s(dest, destsz, src, count) strncpy(dest, src, destsz)
#define sprintf_s(buffer, bufsz, format, ...) sprintf(buffer, format, __VA_ARGS__)
#endif

#if !defined(_MSC_VER) || (defined(_MSC_VER) && (defined(_CRT_NONSTDC_NO_WARNINGS) || !defined(_CRT_INTERNAL_NONSTDC_NAMES) || (defined(_CRT_INTERNAL_NONSTDC_NAMES) && !_CRT_INTERNAL_NONSTDC_NAMES)))
#define _fileno(file) fileno(file)
#define _isatty(fd) isatty(fd)
#endif

#include <chrono>
#include <ctime>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <iomanip>

#include <atomic>
#include <mutex>
#include <thread>

#include <memory>
#include <new>

#include <sstream>
#include <string>
#include <string_view>

#include <algorithm>
#include <functional>
#include <utility>
#include <random>

#include <set>
#include <unordered_set>
#include <stack>
#include <vector>

#include <typeinfo>
#include <type_traits>

#include <exception>
#include <stdexcept>

#include <any>
#include <optional>
#include <variant>

#include <format>
#include <nlohmann/json.hpp>

#include "logger/logger.hpp"

#include "core/settings.hpp"
#include "ped/CPed.hpp"

#include "services/notifications/notification_service.hpp"
#include "services/translation_service/translation_service.hpp"

#include "lua/sol_include.hpp"

#include <script/types.hpp>

// clang-format on

namespace big
{
	using namespace std::chrono_literals;

	inline HMODULE g_hmodule{};
	inline HANDLE g_main_thread{};
	inline DWORD g_main_thread_id{};
	inline std::atomic_bool g_running{false};

	inline CPed* g_local_player;
}

namespace self
{
	inline Ped ped;
	inline Player id;
	inline Vector3 pos;
	inline Vector3 rot;
	inline Vehicle veh;
	inline int char_index;
	inline std::unordered_set<int> spawned_vehicles;
}

template<size_t N>
struct template_str
{
	constexpr template_str(const char (&str)[N])
	{
		std::copy_n(str, N, value);
	}

	char value[N];
};

#endif
