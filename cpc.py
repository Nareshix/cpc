#!/usr/bin/env python3

import argparse
import sys
import subprocess
from pathlib import Path

def copy_to_clipboard(text: str):
    """Copies text to the Wayland clipboard using wl-copy."""
    try:
        subprocess.run(['wl-copy'], input=text, text=True, check=True)
        return True
    except FileNotFoundError:
        print("Error: 'wl-copy' command not found. Is wl-clipboard installed?", file=sys.stderr)
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error: 'wl-copy' failed: {e}", file=sys.stderr)
        return False

def generate_tree(dir_path: Path, prefix: str = "", excludes: list = None):
    """
    Natively generates a directory tree structure in Python.
    This is a pure Python replacement for the 'tree' command.
    """
    if excludes is None:
        excludes = []
    
    # Get all items in the directory, filter out excluded ones, and sort them
    items = [item for item in dir_path.iterdir() if not any(ex in str(item) for ex in excludes)]
    items.sort(key=lambda x: (x.is_file(), x.name.lower())) # Dirs first, then files

    # Use a list for efficient string building
    tree_lines = []
    for i, item in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        tree_lines.append(f"{prefix}{connector}{item.name}")

        if item.is_dir():
            # The new prefix for children depends on whether the current item is the last one
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_lines.append(generate_tree(item, prefix=new_prefix, excludes=excludes))
    
    return "\n".join(tree_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Copy file or directory contents to the clipboard.",
        epilog="Example: cpc.py src/ --exclude node_modules --exclude .git"
    )
    parser.add_argument("input", help="The file or directory to process.")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Pattern to exclude. Any path containing this string will be ignored."
    )
    parser.add_argument(
        "--tree",
        action="store_true",
        help="Copy the output of a native tree command for the given directory."
    )

    args = parser.parse_args()
    input_path = Path(args.input).resolve() # Use absolute paths for clarity

    # --- Tree Mode (Native Implementation) ---
    if args.tree:
        if not input_path.is_dir():
            print(f"Error: '{args.input}' is not a directory for --tree mode.", file=sys.stderr)
            sys.exit(1)
        
        # Start the tree with the root directory name
        tree_output = f"{input_path.name}\n"
        tree_output += generate_tree(input_path, excludes=args.exclude)
        
        if copy_to_clipboard(tree_output):
            print(tree_output)
            print(f"\nCopied tree output of directory '{args.input}' to clipboard.")
        sys.exit(0)

    # --- File Mode ---
    if input_path.is_file():
        try:
            content = input_path.read_text(encoding='utf-8')
            if copy_to_clipboard(content):
                print("Copied:")
                print()
                print(content)
        except Exception as e:
            print(f"Error reading file '{input_path}': {e}", file=sys.stderr)
            sys.exit(1)

    # --- Directory Mode (Native Implementation) ---
    elif input_path.is_dir():
        output_parts = []
        # Use rglob to recursively find all files, replacing the 'find' command
        all_files = sorted(input_path.rglob('*'))

        for file in all_files:
            # Skip directories
            if not file.is_file():
                continue

            # Check for excluded patterns in the full path
            if any(pattern in str(file) for pattern in args.exclude):
                continue

            try:
                # Get a clean, relative path for the header
                relative_path = file.relative_to(input_path.parent)
                header = f"file: {relative_path}\ncontents:"
                contents = file.read_text(encoding='utf-8', errors='ignore')
                output_parts.append(f"{header}\n{contents}")
            except Exception as e:
                print(f"Warning: Could not read file '{file}': {e}", file=sys.stderr)
                continue
        
        final_output = "\n\n".join(output_parts)
        
        if final_output and copy_to_clipboard(final_output):
            print(final_output)
            print("\nAll files copied to clipboard.")
        elif not final_output:
            print("No files found to copy (or all were excluded).")

    # --- Not Found ---
    else:
        print(f"Error: '{args.input}' is not a valid file or directory.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
