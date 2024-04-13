cmake_minimum_required(VERSION 3.20)

project(YimMenu CXX ASM_MASM)

set(SRC_DIR "${PROJECT_SOURCE_DIR}/src")

# Git commit embed
include(cmake/git.cmake)

# Fetch modules
message("\nFetching modules")
include(cmake/minhook.cmake)
include(cmake/async-logger.cmake)
include(cmake/pugixml.cmake)
include(cmake/json.cmake)
include(cmake/cpr.cmake)
include(cmake/lua.cmake)
include(cmake/imgui.cmake)
message("\nFetching custom modules")
include(cmake/gtav-classes.cmake)

# Build options
include(cmake/build_options.cmake)

# YimMenu
message(STATUS "YimMenu")
file(GLOB_RECURSE SRC_MAIN
  "${SRC_DIR}/**.hpp"
  "${SRC_DIR}/**.h"
  "${SRC_DIR}/**.cpp"
  "${SRC_DIR}/**.cc"
  "${SRC_DIR}/**.cxx"
  "${SRC_DIR}/**.asm"
)

# Actually use build options
include(cmake/build_options_impl.cmake)

add_library(YimMenu MODULE "${SRC_MAIN}")

set_property(GLOBAL PROPERTY USE_FOLDERS ON)
set_property(TARGET YimMenu PROPERTY CXX_STANDARD 23)
set_property(TARGET YimMenu PROPERTY CXX_STANDARD_REQUIRED ON)
set_property(TARGET YimMenu PROPERTY CXX_EXTENSIONS OFF)

source_group(TREE ${SRC_DIR} PREFIX "src" FILES ${SRC_MAIN} )

target_include_directories(YimMenu PRIVATE 
  "${SRC_DIR}"
  "${json_SOURCE_DIR}/single_include"
  "${gtav_classes_SOURCE_DIR}"
  "${imgui_SOURCE_DIR}"
  "${minhook_SOURCE_DIR}/src/hde"
)

target_precompile_headers(YimMenu PRIVATE "${SRC_DIR}/common.hpp")
target_link_libraries(YimMenu PRIVATE pugixml minhook AsyncLogger dbghelp imgui cpr lua_static)

add_compile_definitions(YimMenu
  "NOMINMAX"
  "WIN32_LEAN_AND_MEAN"
)

# Generate a JSON compilation database
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
