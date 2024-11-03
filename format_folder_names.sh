#!/bin/zsh

# Use the provided directory as the target, or default to the current directory
target_dir="${1:-.}"

# Check if the target is a valid directory
if [[ -d "$target_dir" ]]; then
  # List all subdirectories with "- " prepended
  for dir in "$target_dir"/*(/); do
    # Strip the path, leaving only the folder name
    folder_name="${dir##*/}"
    echo "- $folder_name"
  done
else
  echo "Error: '$target_dir' is not a valid directory."
  exit 1
fi
