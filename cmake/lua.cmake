include(FetchContent)

FetchContent_Declare(
    Lua
    GIT_REPOSITORY https://github.com/walterschell/Lua.git
    GIT_TAG        88246d621abf7b6fba9332f49229d507f020e450
    GIT_PROGRESS   TRUE
)
message("Lua")
FetchContent_MakeAvailable(Lua)
set_property(TARGET lua_static PROPERTY C_STANDARD 99)
