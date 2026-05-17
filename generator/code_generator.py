import os
import re

def parse_idl(file_path):
    """
    Parses a simple IDL file and extracts the service name and methods.
    Returns:
        service_name (str),
        methods (list of dicts with 'name' and 'params')
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Match: service ServiceName { ... }
    service_match = re.search(r'service\s+(\w+)\s*\{([^}]+)\}', content)
    if not service_match:
        raise ValueError("Invalid IDL format: Could not find 'service ServiceName { ... }'")

    service_name = service_match.group(1)
    methods_block = service_match.group(2)

    methods = []
    # Match: method_name(type arg1, type arg2)
    # E.g. add(int a, int b)
    method_pattern = re.compile(r'(\w+)\s*\(([^)]*)\)')
    for match in method_pattern.finditer(methods_block):
        method_name = match.group(1)
        params_str = match.group(2).strip()
        
        params = []
        if params_str:
            for p in params_str.split(','):
                p = p.strip()
                if p:
                    # e.g., 'int a' -> type='int', name='a'
                    parts = p.split()
                    if len(parts) == 2:
                        params.append({'type': parts[0], 'name': parts[1]})
                    else:
                        # Fallback if just name is provided
                        params.append({'name': parts[0]})
        
        methods.append({
            'name': method_name,
            'params': params
        })

    return service_name, methods

def generate_stub(service_name, methods, output_path):
    """Generates the client-side stub."""
    lines = [
        "# ==========================================",
        "# AUTO-GENERATED STUB FILE. DO NOT MODIFY.",
        "# ==========================================",
        "",
        f"class {service_name}Stub:",
        "    def __init__(self, rpc_client):",
        "        self.rpc_client = rpc_client",
        ""
    ]

    for m in methods:
        method_name = m['name']
        param_names = [p['name'] for p in m['params']]
        
        # Method signature
        args_str = ", ".join(["self"] + param_names)
        lines.append(f"    def {method_name}({args_str}):")
        
        # RPC Call
        if param_names:
            call_args = ", ".join([f'"{method_name}"'] + param_names)
        else:
            call_args = f'"{method_name}"'
            
        lines.append(f"        return self.rpc_client.call({call_args})")
        lines.append("")

    with open(output_path, 'w') as f:
        f.write("\n".join(lines))
    print(f"[*] Generated Stub -> {output_path}")

def generate_skeleton(service_name, methods, output_path):
    """Generates the server-side skeleton."""
    lines = [
        "# ==========================================",
        "# AUTO-GENERATED SKELETON FILE. DO NOT MODIFY.",
        "# ==========================================",
        "",
        f"class {service_name}Skeleton:",
        "    def __init__(self, rpc_server, service_impl):",
        "        self.rpc_server = rpc_server",
        "        self.service_impl = service_impl",
        "        self._register_methods()",
        "",
        "    def _register_methods(self):"
    ]

    for m in methods:
        method_name = m['name']
        lines.append(f"        self.rpc_server.register_function(self.service_impl.{method_name}, \"{method_name}\")")

    lines.append("")

    with open(output_path, 'w') as f:
        f.write("\n".join(lines))
    print(f"[*] Generated Skeleton -> {output_path}")

if __name__ == "__main__":
    # Define paths relative to the project root
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    idl_path = os.path.join(base_dir, 'idl', 'calculator.idl')
    stub_path = os.path.join(base_dir, 'client', 'generated_stub.py')
    skeleton_path = os.path.join(base_dir, 'server', 'generated_skeleton.py')

    try:
        service_name, methods = parse_idl(idl_path)
        print(f"[*] Parsed IDL: Service '{service_name}' with {len(methods)} methods.")
        
        generate_stub(service_name, methods, stub_path)
        generate_skeleton(service_name, methods, skeleton_path)
        
        print("[*] Generation complete!")
    except Exception as e:
        print(f"[-] Code generation failed: {e}")
