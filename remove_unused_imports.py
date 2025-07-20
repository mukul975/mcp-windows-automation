#!/usr/bin/env python3
"""
Script to detect and remove unused imports from unified_server.py
Uses Python's ast module to analyze the code without external dependencies.
"""
import ast
import re
from typing import Set, Dict, List, Tuple

def parse_imports(file_content: str) -> Dict[str, List[Tuple[int, str]]]:
    """Parse all imports from the file and return them with line numbers."""
    tree = ast.parse(file_content)
    imports = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            line_no = node.lineno
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                if name not in imports:
                    imports[name] = []
                imports[name].append((line_no, f"import {alias.name}"))
        elif isinstance(node, ast.ImportFrom):
            line_no = node.lineno
            module = node.module or ""
            for alias in node.names:
                name = alias.asname if alias.asname else alias.name
                if name not in imports:
                    imports[name] = []
                import_line = f"from {module} import {alias.name}"
                if alias.asname:
                    import_line += f" as {alias.asname}"
                imports[name].append((line_no, import_line))
    
    return imports

def find_used_names(file_content: str) -> Set[str]:
    """Find all names that are actually used in the code."""
    tree = ast.parse(file_content)
    used_names = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)
        elif isinstance(node, ast.Attribute):
            # For attribute access like os.path, we want to track 'os'
            if isinstance(node.value, ast.Name):
                used_names.add(node.value.id)
    
    return used_names

def remove_unused_imports(file_path: str, dry_run: bool = True) -> None:
    """Remove unused imports from the specified file."""
    print(f"Analyzing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Parse imports and find used names
    imports = parse_imports(content)
    used_names = find_used_names(content)
    
    # Find unused imports
    unused_imports = []
    for name, import_info in imports.items():
        if name not in used_names:
            unused_imports.extend(import_info)
    
    # Sort by line number (descending so we can remove from bottom up)
    unused_imports.sort(key=lambda x: x[0], reverse=True)
    
    print(f"\nFound {len(unused_imports)} potentially unused import lines:")
    for line_no, import_stmt in unused_imports:
        print(f"  Line {line_no}: {import_stmt}")
    
    if not dry_run and unused_imports:
        # Remove the lines (working backwards to maintain line numbers)
        for line_no, _ in unused_imports:
            if 1 <= line_no <= len(lines):
                lines[line_no - 1] = ""  # Mark for removal
        
        # Remove empty lines and clean up
        cleaned_lines = []
        for line in lines:
            if line.strip() == "":
                if not cleaned_lines or cleaned_lines[-1].strip() != "":
                    cleaned_lines.append("")
            else:
                cleaned_lines.append(line)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cleaned_lines))
        
        print(f"\nRemoved {len(unused_imports)} unused import lines from {file_path}")
    elif dry_run:
        print(f"\nDRY RUN: Would remove {len(unused_imports)} unused import lines")
        print("Run with dry_run=False to actually remove the imports")

if __name__ == "__main__":
    # Run analysis on unified_server.py
    remove_unused_imports("unified_server.py", dry_run=False)
