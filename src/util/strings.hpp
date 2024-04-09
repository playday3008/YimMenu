#pragma once

#include <locale>

namespace big::strings
{
	namespace comparisons
	{
		template<typename T>
		bool iequals(std::basic_string_view<T> lhs, std::basic_string_view<T> rhs)
		{
			auto n = lhs.size();
			if (rhs.size() != n)
				return false;
			auto p1 = lhs.data();
			auto p2 = rhs.data();
			T a, b;
			while (n--)
			{
				a = *p1++;
				b = *p2++;
				if (a != b)
				{
					if (std::tolower(a) != std::tolower(b))
						return false;
				}
			}
			return true;
		}

		template<typename T>
		struct iequal
		{
			bool operator()(std::basic_string_view<T> lhs, std::basic_string_view<T> rhs) const
			{
				return iequals(lhs, rhs);
			}
		};
	}

	namespace conversions
	{
		inline std::string utf_16_to_code_page(uint32_t code_page, std::wstring_view input)
		{
			if (input.empty())
				return {};

			const auto size = WideCharToMultiByte(code_page, 0, input.data(), static_cast<int>(input.size()), nullptr, 0, nullptr, nullptr);

			std::string output(size, '\0');

			if (size
			    != WideCharToMultiByte(code_page,
			        0,
			        input.data(),
			        static_cast<int>(input.size()),
			        output.data(),
			        static_cast<int>(output.size()),
			        nullptr,
			        nullptr))
			{
				const auto error_code = GetLastError();
				LOG(WARNING) << "WideCharToMultiByte Error in String " << error_code;
				return {};
			}

			return output;
		}
	}
}
