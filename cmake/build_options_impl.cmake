if(MSVC)
  # Global compiler settings
  set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
    /W3 # Enable all warnings

    # Code generation
    /GF # Enable string pooling. (Eliminates duplicate strings)
    /GS # Buffer security check

    # Miscellaneous
    /bigobj # Required for large projects
    /utf-8 # Use UTF-8

    # Diagnostics
    /sdl- # Disable additional security features
  )

  if(ENABLE_NATIVE)
    if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
      message(WARNING "Native architecture is not supported on MSVC, using default architecture instead")
      set(ENABLE_NATIVE OFF)
    elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        -march=native # Enable all available instruction sets
      )
    else()
      message(FATAL_ERROR "Unknown compiler: ${CMAKE_CXX_COMPILER_ID}")
    endif()
  endif()
  if(ENABLE_AVX512 AND NOT ENABLE_NATIVE)
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      /arch:AVX512 # Enable AVX-512 instructions
    )
  elseif(ENABLE_AVX2 AND NOT ENABLE_NATIVE)
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      /arch:AVX2 # Enable AVX2 instructions
    )
  elseif(ENABLE_AVX AND NOT ENABLE_NATIVE)
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      /arch:AVX # Enable AVX instructions
    )
  endif()

  # Veriant specific compiler settings
  if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_VS_JUST_MY_CODE_DEBUGGING ON CACHE BOOL "Just My Code Debugging")
  else()
    # Global Release compiler settings
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      /Oi # Enable intrinsic functions
      /Oy # Omit frame pointers
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
    elseif(CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        /Os # Favor small code
      )
    elseif(CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        /Ot # Favor fast code
      )
    else()
      message(FATAL_ERROR "Unknown build type: ${CMAKE_BUILD_TYPE}")
    endif()
  endif()

  # Real MSVC
  if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
    # Global compiler settings for MSVC
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      # Miscellaneous
      /MP # Parallelize compilation
    )

    # Veriant specific compiler settings
    if(CMAKE_BUILD_TYPE STREQUAL "Debug")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        /Zf # Enable faster PDB generation
      )
    else()
      # Global Release compiler settings
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        #/Ob3 # Inline any suitable function
        /GL # Whole program optimization
      )

      # Variant specific Release compiler settings
      if(CMAKE_BUILD_TYPE STREQUAL "Release")
        string(REPLACE "/Ob2" "/Ob3" CMAKE_CXX_FLAGS_RELEASE ${CMAKE_CXX_FLAGS_RELEASE})
      elseif(CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
        string(REPLACE "/Ob1" "/Ob3" CMAKE_CXX_FLAGS_MINSIZEREL ${CMAKE_CXX_FLAGS_MINSIZEREL})
      elseif(CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
        string(REPLACE "/Ob1" "/Ob3" CMAKE_CXX_FLAGS_RELWITHDEBINFO ${CMAKE_CXX_FLAGS_RELWITHDEBINFO})
      else()
        message(FATAL_ERROR "Unknown build type: ${CMAKE_BUILD_TYPE}")
      endif()
    endif()
  # Clang-cl
  elseif("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
    # Global compiler settings for Clang
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
    
    )

    # Veriant specific compiler settings
    if(CMAKE_BUILD_TYPE STREQUAL "Debug")

    else()
      # Global Release compiler settings
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      
      )

      # Variant specific Release compiler settings
      if(CMAKE_BUILD_TYPE STREQUAL "Release")
        set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
          -s
        )
      elseif(CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
        set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
          -s
        )
        string(REPLACE "/Ob1" "/Ob2" CMAKE_CXX_FLAGS_MINSIZEREL ${CMAKE_CXX_FLAGS_MINSIZEREL})
      elseif(CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
        string(REPLACE "/Ob1" "/Ob2" CMAKE_CXX_FLAGS_RELWITHDEBINFO ${CMAKE_CXX_FLAGS_RELWITHDEBINFO})
      else()
        message(FATAL_ERROR "Unknown build type: ${CMAKE_BUILD_TYPE}")
      endif()
    endif()

    # Dirty hack to disable warnings for specific targets
    target_compile_options(cpr PRIVATE
      -Wno-error
    )
  else()
    message(FATAL_ERROR "Unknown compiler: ${CMAKE_CXX_COMPILER_ID}")
  endif()

  set(_CMAKE_C_COMPILE_OPTIONS ${_CMAKE_C_COMPILE_OPTIONS} ${_CMAKE_C_CXX_COMPILE_OPTIONS})
  set(_CMAKE_CXX_COMPILE_OPTIONS ${_CMAKE_CXX_COMPILE_OPTIONS} ${_CMAKE_C_CXX_COMPILE_OPTIONS})
  set(_CMAKE_C_LINK_OPTIONS ${_CMAKE_C_LINK_OPTIONS} ${_CMAKE_C_CXX_LINK_OPTIONS})
  set(_CMAKE_CXX_LINK_OPTIONS ${_CMAKE_CXX_LINK_OPTIONS} ${_CMAKE_C_CXX_LINK_OPTIONS})
else()
  # Global compiler settings
  set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
    -Wall # Enable all warnings
    -Wextra # Enable extra warnings
  
    # Code generation
    -fstack-protector-strong # Enable stack protection
  
    # Miscellaneous
    -Wa,-mbig-obj
    -fuse-ld=lld # Use lld linker
  )

  if(ENABLE_NATIVE)
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        -march=native # Enable all available instruction sets
      )
  elseif(ENABLE_AVX512)
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      -mavx512f # Enable AVX-512 instructions
      -mavx512dq
      -mavx512cd
      -mavx512bw
      -mavx512vl
    )
  elseif(ENABLE_AVX2)
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      -mavx2 # Enable AVX2 instructions
    )
  elseif(ENABLE_AVX)
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      -mavx # Enable AVX instructions
    )
  endif()

  # Veriant specific compiler settings
  if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      -fjmc # Enable just my code debugging
    )
  else()
    # Global Release compiler settings
    set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
      -fbuiltin # Enable builtin functions
      -fomit-frame-pointer # Omit frame pointers
      -flto # Enable link-time optimization
      -fwhole-program-vtables # Use whole program vtables optimization
      -fdata-sections # Place each function or data item into its own section
    )

    # Variant specific Release compiler settings
    if(CMAKE_BUILD_TYPE STREQUAL "Release")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        -s
      )
    elseif(CMAKE_BUILD_TYPE STREQUAL "MinSizeRel")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}
        -s
      )
    elseif(CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
      set(_CMAKE_C_CXX_COMPILE_OPTIONS ${_CMAKE_C_CXX_COMPILE_OPTIONS}

      )
    else()
      message(FATAL_ERROR "Unknown build type: ${CMAKE_BUILD_TYPE}")
    endif()
  endif()

  set(_CMAKE_C_COMPILE_OPTIONS ${_CMAKE_C_COMPILE_OPTIONS} ${_CMAKE_C_CXX_COMPILE_OPTIONS})
  set(_CMAKE_CXX_COMPILE_OPTIONS ${_CMAKE_CXX_COMPILE_OPTIONS} ${_CMAKE_C_CXX_COMPILE_OPTIONS})
  set(_CMAKE_C_LINK_OPTIONS ${_CMAKE_C_LINK_OPTIONS} ${_CMAKE_C_CXX_LINK_OPTIONS})
  set(_CMAKE_CXX_LINK_OPTIONS ${_CMAKE_CXX_LINK_OPTIONS} ${_CMAKE_C_CXX_LINK_OPTIONS})
endif()

set(_CMAKE_ASM_MASM_COMPILE_OPTIONS ${_CMAKE_ASM_MASM_COMPILE_OPTIONS}
  /nologo # Suppress startup banner
)

add_compile_options(
  "$<$<COMPILE_LANGUAGE:ASM_MASM>:${_CMAKE_ASM_MASM_COMPILE_OPTIONS}>"
  "$<$<COMPILE_LANGUAGE:C>:${_CMAKE_C_COMPILE_OPTIONS}>"
  "$<$<COMPILE_LANGUAGE:CXX>:${_CMAKE_CXX_COMPILE_OPTIONS}>"
)

add_link_options(
  "$<$<COMPILE_LANGUAGE:ASM_MASM>:${_CMAKE_ASM_MASM_LINK_OPTIONS}>"
  "$<$<COMPILE_LANGUAGE:C>:${_CMAKE_C_LINK_OPTIONS}>"
  "$<$<COMPILE_LANGUAGE:CXX>:${_CMAKE_CXX_LINK_OPTIONS}>"
)
