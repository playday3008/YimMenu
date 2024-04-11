#pragma once
#include "env.hpp"
#include "memory/module.hpp"

namespace big
{
	inline std::optional<std::string> wine_get_version()
	{
		static auto module = memory::module("ntdll.dll");

		// https://github.com/wine-mirror/wine/blob/00198c4084a61f65f18574d16833d945e50c0614/dlls/ntdll/version.c#L221
		static auto wine_get_version_fn = module.get_export("wine_get_version");
		if (!wine_get_version_fn)
			return std::nullopt;

		static const auto wine_get_version_ptr = wine_get_version_fn.as<std::uintptr_t>();
		static const auto wine_get_version     = reinterpret_cast<const char * CDECL (*)()>(wine_get_version_ptr);

		return wine_get_version();
	}

	inline std::optional<std::string> wine_get_build_id()
	{
		static auto module = memory::module("ntdll.dll");

		// https://github.com/wine-mirror/wine/blob/00198c4084a61f65f18574d16833d945e50c0614/dlls/ntdll/version.c#L230
		static auto wine_get_build_id_fn = module.get_export("wine_get_build_id");
		if (!wine_get_build_id_fn)
			return std::nullopt;

		static const auto wine_get_build_id_ptr = wine_get_build_id_fn.as<std::uintptr_t>();
		static const auto wine_get_build_id     = reinterpret_cast<const char * CDECL (*)()>(wine_get_build_id_ptr);

		return wine_get_build_id();
	}

	inline std::optional<std::tuple<std::string, std::string>> wine_get_host_version()
	{
		static auto module = memory::module("ntdll.dll");

		// https://github.com/wine-mirror/wine/blob/00198c4084a61f65f18574d16833d945e50c0614/dlls/ntdll/version.c#L241
		static auto wine_get_host_version_fn = module.get_export("wine_get_host_version");
		if (!wine_get_host_version_fn)
			return std::nullopt;

		static const auto wine_get_host_version_ptr = wine_get_host_version_fn.as<std::uintptr_t>();
		static const auto wine_get_host_version = reinterpret_cast<const char * CDECL (*)(const char** sysname, const char** release)>(wine_get_host_version_ptr);

		const char *sysname, *release;
		wine_get_host_version(&sysname, &release);

		return std::make_tuple(sysname, release);
	}

	inline bool is_wine()
	{
		return wine_get_version().has_value();
	}

	inline bool is_proton()
	{
		// Proton wouldn't start without this environment variable: https://github.com/ValveSoftware/Proton/blob/bc4d2acf3ba8c3edd8ba915e520996ed811eaf3c/proton#L1496C13-L1496C35
		static const auto steam_compatible = env::get("STEAM_COMPAT_DATA_PATH");

		return is_wine() && steam_compatible;
	}
}
