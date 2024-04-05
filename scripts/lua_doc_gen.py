# working dir: scripts
# python ./lua_doc_gen.py

from __future__ import annotations
from dataclasses import dataclass

import io
import os
from enum import Enum
from typing import Optional

DOCS_FOLDER = "../docs/"
SRC_FOLDER = "../src/"

LUA_API_COMMENT_IDENTIFIER = "lua api"
LUA_API_COMMENT_SEPARATOR = ":"

tables: dict[str, Table] = {}
classes: dict[str, Class] = {}
functions: dict[str, Function] = {}
tabs_enum: list[str] = []
infraction_enum: list[str] = []


class DocKind(Enum):
    Table = "table"
    Class = "class"
    Field = "field"
    Constructor = "constructor"
    Function = "function"
    Tabs = "tabs"
    Infraction = "infraction"


class Table:
    def __init__(
        self,
        name: str,
        fields: list[Field],
        functions: list[Function],
        description: str,
    ) -> None:
        self.name = name.strip()
        self.fields = fields
        self.functions = functions
        self.description = description

    def __str__(self) -> str:
        s = f"# Table: {self.name}\n"
        s += "\n"

        if len(self.description) > 0:
            s += f"{self.description}\n"
            s += "\n"

        if len(self.fields) > 0:
            s += f"## Fields ({len(self.fields)})\n"
            s += "\n"

            self.check_for_duplicate_fields_names()

            for field in self.fields:
                s += field.print_markdown()

        if len(self.functions) > 0:
            s += f"## Functions ({len(self.functions)})\n"
            s += "\n"

            for func in self.functions:
                s += func.print_markdown(f"{self.name}.")

        # Pop the last newline
        s = s[:-1]

        return s

    def check_for_duplicate_fields_names(self) -> None:
        seen: set[str] = set()
        duplicates = [x for x in self.fields if x.name in seen or seen.add(x.name)]
        if len(duplicates) > 0:
            print("Error while building lua doc. Duplicate field names:")
            for dup in duplicates:
                print(dup)
            exit(1)


class Class:
    def __init__(
        self,
        name: str,
        inheritance: list[Class],
        fields: list[Field],
        constructors: list[Constructor],
        functions: list[Function],
        description: str,
    ) -> None:
        self.name = name.strip()
        self.inheritance = inheritance
        self.fields = fields
        self.constructors = constructors
        self.functions = functions
        self.description = description

    def __str__(self) -> str:
        s = f"# Class: {self.name}\n"
        s += "\n"

        if len(self.inheritance) > 0:
            inherited_class_names = ", ".join(c.name for c in self.inheritance)
            s += f"## Inherit from {len(self.inheritance)} class: {inherited_class_names}\n"
            s += "\n"

        if len(self.description) > 0:
            s += f"{self.description}\n"
            s += "\n"

        if len(self.fields) > 0:
            s += f"## Fields ({len(self.fields)})\n"
            s += "\n"

            self.check_for_duplicate_fields_names()

            for field in self.fields:
                s += field.print_markdown()

        if len(self.constructors) > 0:
            s += f"## Constructors ({len(self.constructors)})\n"
            s += "\n"

            for ctor in self.constructors:
                s += ctor.print_markdown()

        if len(self.functions) > 0:
            s += f"## Functions ({len(self.functions)})\n"
            s += "\n"

            for func in self.functions:
                s += func.print_markdown(f"{self.name}:")

        # Pop the last newline
        s = s[:-1]

        return s

    def check_for_duplicate_fields_names(self) -> None:
        seen: set[str] = set()
        duplicates = [x for x in self.fields if x.name in seen or seen.add(x.name)]
        if len(duplicates) > 0:
            print("Error while building lua doc. Duplicate field names:")
            for dup in duplicates:
                print(dup)
            exit(1)


class Field:
    def __init__(self, name: str, type: str, description: str) -> None:
        self.name = name.strip()
        self.type = type.strip()
        self.description = description

    def __str__(self) -> str:
        s = f"Field: {self.name}\n"
        s += f"Type: {self.type}\n"
        s += f"Description: {self.description.strip()}\n"
        return s

    def print_markdown(self) -> str:
        s = ""

        s += f"### `{self.name}`\n"
        s += "\n"

        if len(self.description) > 0:
            s += f"{self.description}\n"
            s += "\n"

        if len(self.type) > 0:
            s += f"- Type: `{self.type}`\n"

        s += "\n"

        return s


class Constructor:
    def __init__(
        self, parent: Class, parameters: list[Parameter], description: str
    ) -> None:
        self.parent = parent
        self.parameters = parameters
        self.description = description

    def print_markdown(self) -> str:
        s = ""

        parameters_str = ", ".join(p.name for p in self.parameters)

        s += f"### `new({parameters_str})`\n"
        s += "\n"

        if len(self.description) > 0:
            s += f"{self.description}\n"
            s += "\n"

        if len(self.parameters) > 0:
            s += f"- **Parameters:**\n"
            for param in self.parameters:
                s += f"  - `{param.name}` ({param.type})"
                if len(param.description) > 0:
                    s += f": {param.description}\n"
                else:
                    s += f"\n"
            s += "\n"

        s += f"**Example Usage:**\n\n"
        s += "```lua\n"

        s += f"myInstance = {self.parent.name}:new({parameters_str})\n"

        s += "```\n"
        s += "\n"

        return s


class Parameter:
    def __init__(self, name: str, type: str, description: str) -> None:
        self.name = name.strip()
        self.type = type.strip()
        self.description = description

    def __str__(self) -> str:
        s = f"Parameter: {self.name}\n"
        s += f"Type: {self.type}\n"
        s += f"Description: {self.description.strip()}\n"
        return s


class Function:
    def __init__(
        self,
        name: str,
        parent: Class | Table,
        parameters: list[Parameter],
        return_type: Optional[str],
        return_description: Optional[str],
        description: str,
    ) -> None:
        self.name = name.strip()
        self.parent = parent
        self.parameters = parameters
        self.return_type = return_type
        self.return_description = return_description
        self.description = description

    def __str__(self):
        s = f"Function: {self.name}\n"

        type_name = str(type(self.parent)).split(".")[1][:-2]
        s += f"Parent: {self.parent.name} ({type_name})\n"

        s += f"Parameters: {len(self.parameters)}\n"
        i = 1
        for param in self.parameters:
            s += f"Parameter {i}\n"
            s += str(param) + "\n"
            i += 1

        s += f"Return Type: {self.return_type}\n"
        s += f"Return Description: {self.return_description}\n"

        s += f"Description: {self.description}\n"
        return s

    def print_markdown(self, prefix: str):
        s = ""

        parameters_str = ", ".join(p.name for p in self.parameters)

        s += f"### `{self.name}({parameters_str})`\n"
        s += "\n"

        if len(self.description) > 0:
            s += f"{self.description}\n"
            s += "\n"

        if len(self.parameters) > 0:
            s += f"- **Parameters:**\n"
            for param in self.parameters:
                s += f"  - `{param.name}` ({param.type})"
                if len(param.description) > 0:
                    s += f": {param.description}\n"
                else:
                    s += f"\n"
            s += "\n"

        if self.return_type is not None and len(self.return_type) > 0:
            s += f"- **Returns:**\n"
            s += f"  - `{self.return_type}`: {self.return_description}\n"

            s += "\n"

        s += f"**Example Usage:**\n\n"
        s += "```lua\n"
        if self.return_type is not None and len(self.return_type) > 0:
            s += self.return_type + " = "

        if "Global Table" in prefix:
            prefix = ""
        s += f"{prefix}{self.name}({parameters_str})\n"

        s += "```\n"
        s += "\n"

        return s


def make_table(table_name: str) -> Table:
    if table_name not in tables:
        tables[table_name] = Table(table_name, [], [], "")
    cur_table = tables[table_name]
    return cur_table


def make_class(class_name: str) -> Class:
    if class_name not in classes:
        classes[class_name] = Class(class_name, [], [], [], [], "")
    cur_class = classes[class_name]
    return cur_class


def is_comment_a_lua_api_doc_comment(text_lower: str) -> bool:
    return (
        LUA_API_COMMENT_IDENTIFIER in text_lower
        and LUA_API_COMMENT_SEPARATOR in text_lower
        and "//" in text_lower
    )


def parse_lua_api_doc(folder_path: str) -> None:
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if os.path.splitext(file_name)[1].startswith((".c", ".h")):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    doc_kind: Optional[DocKind] = None
                    cur_table: Optional[Table] = None
                    cur_class: Optional[Class] = None
                    cur_function: Optional[Function] = None
                    cur_field: Optional[Field] = None
                    cur_constructor: Optional[Constructor] = None

                    for line in file:
                        line = line.strip()
                        line_lower = line.lower()
                        if is_comment_a_lua_api_doc_comment(line_lower):
                            doc_kind = DocKind(
                                line.split(LUA_API_COMMENT_SEPARATOR, 1)[1]
                                .strip()
                                .lower()
                            )

                            if (
                                doc_kind is not DocKind.Tabs
                                and doc_kind is not DocKind.Infraction
                            ):
                                continue

                        if doc_kind is not None and "//" in line:
                            match doc_kind:
                                case DocKind.Table:
                                    cur_table = parse_table_doc(
                                        cur_table, line, line_lower
                                    )
                                case DocKind.Class:
                                    cur_class = parse_class_doc(
                                        cur_class, line, line_lower
                                    )
                                case DocKind.Function:
                                    (
                                        cur_function,
                                        cur_table,
                                        cur_class,
                                    ) = parse_function_doc(
                                        cur_function,
                                        cur_table,
                                        cur_class,
                                        line,
                                        line_lower,
                                    )
                                case DocKind.Field:
                                    (cur_field, cur_table, cur_class) = parse_field_doc(
                                        cur_field,
                                        cur_table,
                                        cur_class,
                                        line,
                                        line_lower,
                                    )
                                case DocKind.Constructor:
                                    (
                                        cur_constructor,
                                        cur_class,
                                    ) = parse_constructor_doc(
                                        cur_constructor,
                                        cur_class,
                                        line,
                                        line_lower,
                                    )
                                case DocKind.Tabs:
                                    parse_tabs_doc(file)
                                case DocKind.Infraction:
                                    parse_infraction_doc(file)
                        else:
                            doc_kind = None


def parse_table_doc(
    cur_table: Optional[Table], line: str, line_lower: str
) -> Optional[Table]:
    if is_lua_doc_comment_startswith(line_lower, "name"):
        table_name = line.split(LUA_API_COMMENT_SEPARATOR, 1)[1].strip()
        cur_table = make_table(table_name)
    elif cur_table is not None:
        if len(cur_table.description) != 0:
            cur_table.description += "\n"
        cur_table.description += sanitize_description(line)

    return cur_table


def parse_class_doc(
    cur_class: Optional[Class], line: str, line_lower: str
) -> Optional[Class]:
    if is_lua_doc_comment_startswith(line_lower, "name"):
        class_name = line.split(LUA_API_COMMENT_SEPARATOR, 1)[1].strip()
        cur_class = make_class(class_name)
    elif cur_class is not None and is_lua_doc_comment_startswith(line_lower, "inherit"):
        inherited_class_name = line.split(LUA_API_COMMENT_SEPARATOR, 1)[1].strip()
        cur_class.inheritance.append(make_class(inherited_class_name))
    elif cur_class is not None:
        if len(cur_class.description) != 0:
            cur_class.description += "\n"
        cur_class.description += sanitize_description(line)

    return cur_class


def parse_function_doc(
    cur_function: Optional[Function],
    cur_table: Optional[Table],
    cur_class: Optional[Class],
    line: str,
    line_lower: str,
) -> tuple[Optional[Function], Optional[Table], Optional[Class]]:
    if (
        is_lua_doc_comment_startswith(line_lower, "table")
        and LUA_API_COMMENT_SEPARATOR in line_lower
    ):
        table_name = line.split(LUA_API_COMMENT_SEPARATOR, 1)[1].strip()
        cur_table = make_table(table_name)

        cur_function = Function("Didnt get name yet", cur_table, [], None, None, "")
        cur_table.functions.append(cur_function)
    elif (
        is_lua_doc_comment_startswith(line_lower, "class")
        and LUA_API_COMMENT_SEPARATOR in line_lower
    ):
        class_name = line.split(LUA_API_COMMENT_SEPARATOR, 1)[1].strip()
        cur_class = make_class(class_name)

        cur_function = Function("Didnt get name yet", cur_class, [], None, None, "")
        cur_class.functions.append(cur_function)
    elif (
        is_lua_doc_comment_startswith(line_lower, "name")
        and LUA_API_COMMENT_SEPARATOR in line_lower
        and cur_function is not None
    ):
        function_name = line.split(LUA_API_COMMENT_SEPARATOR, 1)[1].strip()
        cur_function.name = function_name

        if function_name not in functions:
            functions[function_name] = cur_function
    elif (
        is_lua_doc_comment_startswith(line_lower, "param")
        and LUA_API_COMMENT_SEPARATOR in line_lower
        and cur_function is not None
    ):
        parameter = make_parameter_from_doc_line(line)
        cur_function.parameters.append(parameter)
    elif (
        is_lua_doc_comment_startswith(line_lower, "return")
        and LUA_API_COMMENT_SEPARATOR in line_lower
        and cur_function is not None
    ):
        return_info = line.split(LUA_API_COMMENT_SEPARATOR, 2)
        try:
            cur_function.return_type = return_info[1].strip()
            cur_function.return_description = return_info[2].strip()
        except IndexError:
            pass
    elif cur_function is not None:
        if len(cur_function.description) != 0:
            cur_function.description += "\n"
        cur_function.description += sanitize_description(line)

    return cur_function, cur_table, cur_class


def parse_field_doc(
    cur_field: Optional[Field],
    cur_table: Optional[Table],
    cur_class: Optional[Class],
    line: str,
    line_lower: str,
) -> tuple[Optional[Field], Optional[Table], Optional[Class]]:
    if (
        is_lua_doc_comment_startswith(line_lower, "table")
        and LUA_API_COMMENT_SEPARATOR in line_lower
    ):
        table_name = line.split(LUA_API_COMMENT_SEPARATOR, 1)[1].strip()
        cur_table = make_table(table_name)

        cur_field = Field("Didnt get name yet", "", "")
        cur_table.fields.append(cur_field)
    elif (
        is_lua_doc_comment_startswith(line_lower, "class")
        and LUA_API_COMMENT_SEPARATOR in line_lower
    ):
        class_name = line.split(LUA_API_COMMENT_SEPARATOR, 1)[1].strip()
        cur_class = make_class(class_name)

        cur_field = Field("Didnt get name yet", "", "")
        cur_class.fields.append(cur_field)
    elif (
        is_lua_doc_comment_startswith(line_lower, "field")
        and LUA_API_COMMENT_SEPARATOR in line_lower
        and cur_field is not None
    ):
        field_info = line.split(LUA_API_COMMENT_SEPARATOR, 2)
        cur_field.name = field_info[1].strip()
        cur_field.type = field_info[2].strip()
    elif cur_field is not None:
        if len(cur_field.description) != 0:
            cur_field.description += "\n"

        if line.startswith("// "):
            line = line[3:]
        cur_field.description += sanitize_description(line)

    return cur_field, cur_table, cur_class


def parse_constructor_doc(
    cur_constructor: Optional[Constructor],
    cur_class: Optional[Class],
    line: str,
    line_lower: str,
) -> tuple[Optional[Constructor], Optional[Class]]:
    if (
        is_lua_doc_comment_startswith(line_lower, "class")
        and LUA_API_COMMENT_SEPARATOR in line_lower
    ):
        class_name = line.split(LUA_API_COMMENT_SEPARATOR, 1)[1].strip()
        cur_class = make_class(class_name)

        cur_constructor = Constructor(cur_class, [], "")
        cur_class.constructors.append(cur_constructor)
    elif (
        is_lua_doc_comment_startswith(line_lower, "param")
        and LUA_API_COMMENT_SEPARATOR in line_lower
        and cur_constructor is not None
    ):
        parameter = make_parameter_from_doc_line(line)
        cur_constructor.parameters.append(parameter)
    elif cur_constructor is not None:
        if len(cur_constructor.description) != 0:
            cur_constructor.description += "\n"
        cur_constructor.description += sanitize_description(line)

    return cur_constructor, cur_class


def parse_tabs_doc(file: io.TextIOWrapper) -> None:
    start_parsing = False
    for line in file:
        if "enum class" in line.lower():
            start_parsing = True
            continue

        if start_parsing:
            if "};" in line.lower():
                return
            if "{" == line.lower().strip():
                continue
            if "//" in line.lower():
                continue
            if "" == line.lower().strip():
                continue
            else:
                tabs_enum.append(line.replace(",", "").strip())


def parse_infraction_doc(file: io.TextIOWrapper) -> None:
    start_parsing = False
    for line in file:
        if "enum class" in line.lower():
            start_parsing = True
            continue

        if start_parsing:
            if "};" in line.lower():
                return
            if "{" == line.lower().strip():
                continue
            if "//" in line.lower():
                continue
            if "" == line.lower().strip():
                continue
            else:
                infraction_enum.append(line.replace(",", "").strip())


def make_parameter_from_doc_line(line: str) -> Parameter:
    param_info = line.split(LUA_API_COMMENT_SEPARATOR, 3)[1:]
    param_name = param_type = param_desc = ""

    try:
        param_name = param_info[0].strip()
        param_type = param_info[1].strip()
        param_desc = param_info[2].strip()
    except IndexError:
        pass

    return Parameter(param_name, param_type, param_desc)


def sanitize_description(line: str) -> str:
    if line.startswith("// ") and line[3] != " ":
        line = line[3:]
    if line.startswith("//"):
        line = line[2:]
    return line.rstrip()


def is_lua_doc_comment_startswith(line_lower: str, starts_with_text: str) -> bool:
    return line_lower.replace("//", "").strip().startswith(starts_with_text)


@dataclass
class Command:
    name: str
    label: str
    description: str
    arg_count: int


def main() -> None:
    parse_lua_api_doc(SRC_FOLDER)

    # Write the tables to files
    try:
        os.makedirs(DOCS_FOLDER + "lua/tables/")
    except:
        pass

    for table_name, table in tables.items():
        file_name = f"{DOCS_FOLDER}lua/tables/{table_name}.md"
        if os.path.exists(file_name):
            os.remove(file_name)
        f = open(file_name, "ba")
        f.write(bytes(str(table), "UTF8"))
        f.close()

    # Write the tabs to file
    tabs_file_buf = (
        "# Tabs\n"
        "\n"
        "All the tabs from the menu are listed below, used as parameter for adding gui elements to them.\n"
        "\n"
        "**Example Usage:**\n"
        "\n"
        "```lua\n"
        'missionsTab = gui.get_tab("GUI_TAB_MISSIONS")\n'
        'missionsTab:add_button("Click me", function ()\n'
        '    log.info("You clicked!")\n'
        "end)\n"
        "```\n"
        "\n"
        "For a complete list of available gui functions, please refer to the tab class documentation and the gui table documentation.\n"
        "\n"
    )

    tabs_file_buf += "## Tab Count: {len(tabs_enum)}\n\n"

    # Minus the first, because it's the `NONE` tab, minus the last one because it's for runtime defined tabs.
    for i in range(1, len(tabs_enum) - 1):
        tabs_file_buf += "### `GUI_TAB_" + tabs_enum[i] + "`\n\n"
    tabs_file_buf = tabs_file_buf[:-1]

    tabs_file_name = f"{DOCS_FOLDER}lua/tabs.md"
    if os.path.exists(tabs_file_name):
        os.remove(tabs_file_name)
    f = open(tabs_file_name, "a")
    f.write(tabs_file_buf)
    f.close()

    # Write the infraction to file
    infraction_file_buf = (
        "# Infraction\n"
        "\n"
        "All the infraction from the menu are listed below, used as parameter for adding an infraction to a given player, for flagging them as modder.\n"
        "\n"
        "**Example Usage:**\n"
        "\n"
        "```lua\n"
        'network.flag_player_as_modder(player_index, infraction.CUSTOM_REASON, "My custom reason on why the player is flagged as a modder")\n'
        "```\n"
        "\n"
    )

    infraction_file_buf += f"## Infraction Count: {len(infraction_enum)}\n\n"

    for i in range(0, len(infraction_enum)):
        infraction_file_buf += "### `" + infraction_enum[i] + "`\n\n"
    infraction_file_buf = infraction_file_buf[:-1]

    infraction_file_name = f"{DOCS_FOLDER}lua/infraction.md"
    if os.path.exists(infraction_file_name):
        os.remove(infraction_file_name)
    f = open(infraction_file_name, "a")
    f.write(infraction_file_buf)
    f.close()

    # Write the classes to files
    try:
        os.makedirs(DOCS_FOLDER + "lua/classes/")
    except:
        pass

    for class_name, class_ in classes.items():
        file_name = f"{DOCS_FOLDER}lua/classes/{class_name}.md"
        if os.path.exists(file_name):
            os.remove(file_name)
        f = open(file_name, "ba")
        f.write(bytes(str(class_), "UTF8"))
        f.close()

    # Write the commands to files
    commands: list[Command] = []
    with open(DOCS_FOLDER + "lua/commands_dump.txt", "r") as file:
        for line in file:
            cmd = line.split("|", 1)[1].strip().split("|")
            commands.append(
                Command(cmd[0].strip(), cmd[1].strip(), cmd[2].strip(), int(cmd[3]))
            )

    commands_file_buf = (
        "# Commands\n"
        "\n"
        "All the current commands from the menu are listed below.\n"
        "\n"
        "**Example Usage through Lua:**\n"
        "\n"
        "```lua\n"
        'command.call("spawn", {joaat("adder")})\n'
        'command.call_player(somePlayerIndex, "spawn", {joaat("adder")})\n'
        "```\n"
        "\n"
        "For a complete list of available command functions, please refer to the command table documentation.\n"
        "\n"
    )

    commands_file_buf += f"## Command Count: {len(commands)}\n\n"

    for cmd in commands:
        commands_file_buf += f"### `{cmd.name}`\n\n"
        commands_file_buf += f"{cmd.description}\n"
        commands_file_buf += f"Arg Count: {cmd.arg_count}\n"
        commands_file_buf += "\n"
    commands_file_buf = commands_file_buf[:-1]

    commands_file_name = f"{DOCS_FOLDER}lua/commands.md"
    if os.path.exists(commands_file_name):
        os.remove(commands_file_name)
    f = open(commands_file_name, "a")
    f.write(commands_file_buf)
    f.close()


if __name__ == "__main__":
    main()
