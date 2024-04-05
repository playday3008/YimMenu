include(FetchContent)

FetchContent_Declare(
    pugixml
    GIT_REPOSITORY https://github.com/zeux/pugixml.git
    GIT_TAG        v1.14
    GIT_PROGRESS   TRUE
) 
message("pugixml")
FetchContent_MakeAvailable(pugixml)
set_property(TARGET pugixml PROPERTY CXX_STANDARD 11)
