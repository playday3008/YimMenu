#pragma once

#include "common.hpp"

using namespace std::literals;

namespace big::env
{
	inline std::optional<std::string> get(const std::string_view key)
	{
#if defined(__STDC_LIB_EXT1__) || (_MSC_VER >= 1900 && __STDC_WANT_SECURE_LIB__ == 1)
		size_t required_size;

		if (::getenv_s(&required_size, nullptr, 0, key.data()) != 0)
			return std::nullopt;
		else if (required_size == 0)
			return std::nullopt;
		else
		{
			auto buf = std::make_unique<char[]>(required_size);
			::getenv_s(&required_size, buf.get(), required_size, key.data());
			return std::string(buf.get(), required_size - 1);
		}
#else
		return std::string(::getenv(key.data()));
#endif
	}
}
