#!/usr/bin/env bash

# Collect excludes and main input
excludes=()
args=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --exclude)
            shift
            excludes+=("$1")
            ;;
        *)
            args+=("$1")
            ;;
    esac
    shift
done

if [ "${#args[@]}" -ne 1 ]; then
    echo "Usage: cpc <file_or_directory> [--exclude <pattern>]..."
    exit 1
fi

input="${args[0]}"

build_find_exclude_args() {
    local exclude_args=""
    for pattern in "${excludes[@]}"; do
        exclude_args+="! -path '*$pattern*' "
    done
    printf "%s" "$exclude_args"
}

if [ -f "$input" ]; then
    cat "$input" | wl-copy && {
        echo "Copied:"
        echo
        cat "$input"
    } || {
        echo "Error: failed to copy to clipboard."
        exit 1
    }

elif [ -d "$input" ]; then
    output=""
    while IFS= read -r -d '' file; do
        file_output="file: $file"$'\n'"contents:"$'\n'"$(cat "$file")"$'\n'
        echo "$file_output"
        output+="$file_output"$'\n'
    done < <(eval "find \"$input\" -type f $(build_find_exclude_args) -print0")

    echo -n "$output" | wl-copy
    echo "All files copied to clipboard."

else
    echo "'$input' is neither a file nor a directory."
    exit 1
fi
