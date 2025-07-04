import os
import importlib.util
import inspect
import ast

try:
    from . import Config
except ImportError:
    import Config


ENABLED_TOOLS = Config.get("agents")["tools"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(SCRIPT_DIR, "tools")
FUNCTION_TOOLS_MAPPER: dict = {}
# Add Tools dir to system path to enable tool "sub imports"
import sys
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)


# Step 1: List all .py files in the tools folder
def list_py_files() -> list[str]:
    return [f for f in os.listdir(TOOLS_DIR) if f.endswith(".py") and not f.startswith("_")]


# Step 2: Extract function names from a .py file (without importing it)
def list_functions_in_file(file_name: str) -> list[str]:
    absolute_path = os.path.join(TOOLS_DIR, file_name)
    with open(absolute_path, "r", encoding="utf-8") as f:
        node = ast.parse(f.read(), filename=absolute_path)
    return [n.name for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]


# Step 3: Dynamically import a module given its filename
def import_module_from_file(module_filename: str):
    absolute_path = os.path.join(TOOLS_DIR, module_filename)
    module_name = os.path.splitext(module_filename)[0]
    spec = importlib.util.spec_from_file_location(module_name, absolute_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module


def is_tool_enabled(tool_name: str) -> bool:
    if ENABLED_TOOLS is None:
        return True  # If no tools are specified, assume all are enabled.
    if ENABLED_TOOLS and (ENABLED_TOOLS[0] == "*" or ENABLED_TOOLS[0].lower() == "all"):
        if len(ENABLED_TOOLS) > 1 and f"!{tool_name}" in ENABLED_TOOLS:
            return False  # If a tool is explicitly disabled, return False.
        return True  # If all tools are enabled, check individual tool names.
    return tool_name in ENABLED_TOOLS


# Step 4: Build the FUNCTION_TOOLS_MAPPER dict automatically
def generate_tools() -> dict[str, callable]:
    """
    Scans all .py files under TOOLS_DIR, imports them, and
    maps every top-level function name to its function object.
    """
    global FUNCTION_TOOLS_MAPPER
    FUNCTION_TOOLS_MAPPER.clear()

    for filename in list_py_files():
        if not is_tool_enabled(filename):
            continue
        mod = import_module_from_file(filename)
        # Inspect the module for top-level functions
        for name, obj in inspect.getmembers(mod, inspect.isfunction):
            if name.startswith("_"):
                continue
            # Only include functions defined in this module (ignore imports from elsewhere)
            if obj.__module__ == mod.__name__:
                FUNCTION_TOOLS_MAPPER[name] = obj

    return FUNCTION_TOOLS_MAPPER


if __name__ == "__main__":
    # 1. List all .py files in tools/
    py_files = list_py_files()
    print("Available tool modules:", py_files)

    # 2. Pick one (for demonstration, e.g. index 0)
    if not py_files:
        print("No .py files found in tools/ folder.")
        exit(1)

    selected_module = py_files[1]
    print(f"\nSelected module: {selected_module}")

    # 3. List all function names inside that .py file (without importing)
    functions = list_functions_in_file(selected_module)
    print(f"Functions defined in {selected_module} (via AST): {functions}")

    # 5. Build the global FUNCTION_TOOLS_MAPPER dictionary
    mapper = generate_tools()
    print("\nGenerated FUNCTION_TOOLS_MAPPER:")
    for fname, fref in mapper.items():
        print(f"  - {fname} -> {fref}")
