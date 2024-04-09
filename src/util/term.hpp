#pragma once

#include "env.hpp"

#include <io.h>

namespace big::term
{
	inline bool can_do_colors()
	{
		// clang-format off
		return env::get("ANSI_COLORS_DISABLED"sv) || env::get("ANSI_COLOURS_DISABLED"sv) ||
               env::get("NO_COLOR"sv) || env::get("NO_COLOUR"sv) ||
               env::get("TERM"sv) == "dumb" ||
               stdout == nullptr ||
               _fileno(stdout) == -1 ||
               !_isatty(_fileno(stdout));
		// clang-format on
	}
}