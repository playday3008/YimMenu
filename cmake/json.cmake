include(FetchContent)

set(JSON_MultipleHeaders OFF)

FetchContent_Declare(
    json
    URL      https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz
    URL_HASH SHA256=d6c65aca6b1ed68e7a182f4757257b107ae403032760ed6ef121c9d55e81757d
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
message("json")
FetchContent_MakeAvailable(json)
set_property(TARGET nlohmann_json PROPERTY CXX_STANDARD 11)
