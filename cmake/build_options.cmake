# Optimizations
if (MSVC)
    option(ENABLE_NATIVE "Enable Host Native optimizations" OFF)
    option(ENABLE_AVX "Enable AVX optimizations" OFF)
    option(ENABLE_AVX2 "Enable AVX2 optimizations" OFF)
    option(ENABLE_AVX512 "Enable AVX512 optimizations" OFF)
endif()
