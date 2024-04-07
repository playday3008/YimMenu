if (MSVC)
  # Global compiler settings
  set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
    /W3 # Enable all warnings
  
    # Code generation
    /GF # Enable string pooling. (Eliminates duplicate strings)
    /GS # Buffer security check

    # Miscellaneous
    /bigobj # Required for large projects
    /utf-8 # Use UTF-8
    /MP # Parallelize compilation

    # Diagnostics
    /sdl- # Disable additional security features
  )

  if (ENABLE_AVX512)
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      /arch:AVX512 # Enable AVX-512 instructions
    )
  elseif (ENABLE_AVX2)
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      /arch:AVX2 # Enable AVX2 instructions
    )
  elseif (ENABLE_AVX)
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      /arch:AVX # Enable AVX instructions
    )
  endif()

  # Veriant specific compiler settings
  if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_VS_JUST_MY_CODE_DEBUGGING ON CACHE BOOL "Just My Code Debugging")
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      /Zf # Enable faster PDB generation
    )
  else()
    # Global Release compiler settings
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      #/Ob3 # Inline any suitable function
      /Oi # Enable intrinsic functions
      /Oy # Omit frame pointers
      /GL # Whole program optimization
      /Gw # Optimize global data
    )
    set(_CMAKE_C_CXX_LINK_OPTIONS ${_CMAKE_C_CXX_LINK_OPTIONS}
      /OPT:REF # Eliminate functions and data that are never referenced
      /OPT:ICF # Perform identical COMDAT folding
      /LTCG:incremental # Incremental link-time code generation
    )

    # Variant specific Release compiler settings
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        /Ot # Favor fast code
      )
      string(REPLACE "/Ob2" "/Ob3" CMAKE_CXX_FLAGS_RELEASE ${CMAKE_CXX_FLAGS_RELEASE})
    elseif(CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        /Os # Favor small code
      )
      string(REPLACE "/Ob1" "/Ob3" CMAKE_CXX_FLAGS_MINSIZEREL ${CMAKE_CXX_FLAGS_MINSIZEREL})
    elseif(CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        /Ot # Favor fast code
      )
      string(REPLACE "/Ob1" "/Ob3" CMAKE_CXX_FLAGS_RELWITHDEBINFO ${CMAKE_CXX_FLAGS_RELWITHDEBINFO})
    else()
      message(FATAL_ERROR "Unknown build type: ${CMAKE_BUILD_TYPE}")
    endif()
  endif()

  set(_CMAKE_C_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS})
  set(_CMAKE_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS})
  set(_CMAKE_C_LINK_OPTIONS ${_CMAKE_C_CXX_LINK_OPTIONS})
  set(_CMAKE_CXX_LINK_OPTIONS ${_CMAKE_C_CXX_LINK_OPTIONS})
endif()

add_compile_options(
  "$<$<COMPILE_LANGUAGE:MASM>:${_CMAKE_MASM_COMPILE_OPTIONS}>"
  "$<$<COMPILE_LANGUAGE:C>:${_CMAKE_C_COMPILE_OPTIONS}>"
  "$<$<COMPILE_LANGUAGE:CXX>:${_CMAKE_CXX_COMPILE_OPTIONS}>"
)

add_link_options(
  "$<$<COMPILE_LANGUAGE:MASM>:${_CMAKE_MASM_LINK_OPTIONS}>"
  "$<$<COMPILE_LANGUAGE:C>:${_CMAKE_C_LINK_OPTIONS}>"
  "$<$<COMPILE_LANGUAGE:CXX>:${_CMAKE_CXX_LINK_OPTIONS}>"
)
