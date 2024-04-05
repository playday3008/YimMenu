# working dir: scripts
# python ./generate_natives.py

import json
import re

# Source files
CROSSMAP_FILE = "crossmap.txt"
NATIVES_FILE = "./gta5-nativedb-data/natives.json"
# Target files
CROSSMAP_HEADER_FILE = "../src/invoker/crossmap.hpp"
NATIVES_HEADER_FILE = "../src/natives.hpp"


class Arg:
    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type

    def __str__(self) -> str:
        return f"{self.type} {self.name}"


class NativeFunction:
    def __init__(
        self,
        namespace: str,
        name: str,
        hash: int,
        args: list[dict[str, str]],
        return_type: str,
    ) -> None:
        self.namespace = namespace
        self.name = name
        self.hash = hash
        self.args: list[Arg] = []
        self.return_type = return_type
        self.native_index = -1
        self.fix_vectors = "false"

        for arg in args:
            self.args.append(Arg(arg["name"], arg["type"]))
            if arg["type"] == "Vector3*":
                self.fix_vectors = "true"

    def get_native_def_str(self) -> str:
        assert self.native_index != -1

        param_decl = ""
        param_pass = ""
        if len(self.args) > 0:
            for arg in self.args:
                param_decl += str(arg) + ", "
                param_pass += arg.name + ", "
            param_decl = param_decl[:-2]
            param_pass = param_pass[:-2]

        return f"FORCEINLINE constexpr {self.return_type} {self.name}({param_decl}) {{ return big::native_invoker::invoke<{self.native_index}, {self.fix_vectors}, {self.return_type}>({param_pass}); }}"


class CrossmapEntry:
    def __init__(self, translated_hash: int) -> None:
        self.hash = translated_hash
        self.native_index = -1


def load_crossmap_data(file: str) -> dict[int, CrossmapEntry]:
    crossmap: dict[int, CrossmapEntry] = {}

    data = open(file).readlines()
    for item in data:
        translation = item.split(",")
        crossmap[int(translation[0], 16)] = CrossmapEntry(int(translation[1], 16))

    return crossmap


def load_natives_data(file: str) -> dict[str, list[NativeFunction]]:
    natives: dict[str, list[NativeFunction]] = {}

    data = json.load(open(file))
    for ns, natives_list in data.items():
        natives[ns] = []
        for hash_str, native_data in natives_list.items():
            natives[ns].append(
                NativeFunction(
                    ns,
                    native_data["name"],
                    int(hash_str, 16),
                    native_data["params"],
                    native_data["return_type"],
                )
            )

    return natives


def allocate_indices(
    natives: dict[str, list[NativeFunction]], crossmap: dict[int, CrossmapEntry]
) -> list[int]:

    current_idx = 0
    crossmap_hash_list: list[int] = []
    for _, n in natives.items():
        for native in n:
            hash = native.hash
            if hash in crossmap:
                crossmap[hash].native_index = current_idx
                native.native_index = current_idx
                crossmap_hash_list.append(crossmap[hash].hash)
                current_idx += 1

    return crossmap_hash_list


def write_crossmap_header(file: str, crossmap_hash_list: list[int]) -> None:
    crossmap_hash_list_formatted = re.sub(
        r" \x7f",
        "",
        ", ".join(
            [
                ("\x7f\n\t\t" if i != 0 and i % 8 == 0 else "") + f"0x{x:016X}"
                for i, x in enumerate(crossmap_hash_list)
            ]
        ),
    )

    replacement_code = re.sub(
        r"^\s{8}",
        "",
        f"""#pragma once
        #include <script/scrNativeHandler.hpp>
        
        namespace big
        {{
        	constexpr std::array<rage::scrNativeHash, {len(crossmap_hash_list)}> g_crossmap = {{
                {crossmap_hash_list_formatted}
            }};
        }}
        """,
        flags=re.MULTILINE,
    )

    open(file, "w+").write(replacement_code)


def write_natives_header(file: str, natives: dict[str, list[NativeFunction]]) -> None:
    natives_buf = ""
    natives_index_buf = ""

    for ns, nvs in natives.items():
        natives_buf += f"namespace {ns}\n{{\n"
        for nat_data in nvs:
            if nat_data.native_index == -1:
                continue

            natives_buf += f"\t{nat_data.get_native_def_str()}\n"
            natives_index_buf += f"\t{nat_data.name} = {nat_data.native_index},\n"
        natives_buf += "}\n\n"

    natives_index_buf = natives_index_buf[:-2]
    natives_buf = natives_buf[:-2]

    replacement_code = re.sub(
        r"^\s{8}",
        "",
        f"""#pragma once
        #include "invoker/invoker.hpp"
        
        enum class NativeIndex
        {{
        {natives_index_buf}
        }};
        
        // clang-format off
        {natives_buf}
        // clang-format on
        """,
        flags=re.MULTILINE,
    )

    open(file, "w+").write(replacement_code)


def main() -> None:
    crossmap = load_crossmap_data(CROSSMAP_FILE)
    natives = load_natives_data(NATIVES_FILE)
    crossmap_hash_list = allocate_indices(natives, crossmap)
    write_crossmap_header(CROSSMAP_HEADER_FILE, crossmap_hash_list)
    write_natives_header(NATIVES_HEADER_FILE, natives)


if __name__ == "__main__":
    main()
