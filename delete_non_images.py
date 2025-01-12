#!/usr/bin/env python3

import os
import sys

# Allowed extensions (in lowercase)
ALLOWED_EXTENSIONS = {'.heic', '.png', '.jpg'}

def remove_unwanted_files(directory):
    """Remove all files in `directory` (recursively) that do not have an allowed extension."""
    for root, _, files in os.walk(directory):
        for filename in files:
            # Get the file's extension, in lowercase
            _, extension = os.path.splitext(filename)
            extension = extension.lower()
            
            # If the file's extension is not in the allowed set, remove it
            if extension not in ALLOWED_EXTENSIONS:
                file_path = os.path.join(root, filename)
                print(f"Deleting: {file_path}")
                os.remove(file_path)

def main():
    # Check for directory argument
    if len(sys.argv) != 2:
        print("Usage: python delete_non_images.py <path_to_directory>")
        sys.exit(1)

    directory_to_scan = sys.argv[1]

    # Ensure the provided path is a directory
    if not os.path.isdir(directory_to_scan):
        print(f"Error: {directory_to_scan} is not a valid directory.")
        sys.exit(1)

    remove_unwanted_files(directory_to_scan)
    print("Done removing files that aren't HEIC, PNG, or JPG.")

if __name__ == "__main__":
    main()

