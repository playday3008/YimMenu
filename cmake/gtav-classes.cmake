include(FetchContent)

FetchContent_Declare(
    gtav_classes
    GIT_REPOSITORY https://github.com/Yimura/GTAV-Classes.git
    GIT_TAG        052dbff3bef5654c757938d95b4eb7ef42482673
    GIT_PROGRESS   TRUE
)
message("GTAV-Classes")
FetchContent_MakeAvailable(gtav_classes)
set_property(TARGET GTAV-Classes PROPERTY CXX_STANDARD 20)
