include(FetchContent)

FetchContent_Declare(
    AsyncLogger
    GIT_REPOSITORY https://github.com/Yimura/AsyncLogger.git
    GIT_TAG        v0.0.6
    GIT_PROGRESS   TRUE
)
message("AsyncLogger")
FetchContent_MakeAvailable(AsyncLogger)
set_property(TARGET AsyncLogger PROPERTY CXX_STANDARD 20)
