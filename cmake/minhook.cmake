include(FetchContent)

FetchContent_Declare(
    minhook
    GIT_REPOSITORY https://github.com/TsudaKageyu/minhook.git
    GIT_TAG        1cc46107ee522d7a5c73656c519ca16addf2c23a # Last release is heavily outdated, use commit instead
    GIT_PROGRESS   TRUE
)
message("MinHook")
FetchContent_MakeAvailable(minhook)
set_property(TARGET minhook PROPERTY C_STANDARD 11)
