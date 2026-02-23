import argparse
import sys
import subprocess
import os

meta_dictionary = dict()
error_log = []

def main():
    parser = argparse.ArgumentParser(
        prog="Add Meta Data",
        description="Add artist, album, or genre metadata to mp3 files inside a directory or just a file.",
    )

    parser.add_argument('-a', "--artist", nargs=1, type=str, help="Add artist. If artist has a space encase in quotes")
    parser.add_argument('-b', "--album", nargs=1, type=str, help="Add album. If almbum has a space encase in quotes")
    parser.add_argument('-d', "--directories", nargs='+', help="List of directories to go through. This is recursive and will go into subdirectories")
    parser.add_argument('-f', "--files", nargs='+', help="List of files to go through")
    parser.add_argument('-g', "--genre", nargs=1, type=str, help="Add genre. If genre has a space encase in quotes")

    args = parser.parse_args()

    if not args.artist and not args.genre and not args.album:
        print("Need to specify at least one meta flag with -a, -b, or -g", file = sys.stderr)
        sys.exit(1)

    if not args.files and not args.directories:
        print("Need to specify at least one file with -f or directory with -d", file = sys.stderr)
        sys.exit(1)

    if args.artist:
        meta_dictionary["artist"] = args.artist[0]

    if args.genre:
        meta_dictionary["genre"] = args.genre[0]

    if args.album:
        meta_dictionary["album"] = args.album[0]

    if args.files:
        if not validateFiles(args.files):
            sys.exit(1)

        traverseFiles(args.files)

    if args.directories:
        if not validateDirs(args.directories):
            sys.exit(1)

        traverseDirs(args.directories)

    for error in error_log:
        print(error)

# end main

def validateDirs(dir_list):
    assert isinstance(dir_list, list), "Dir list is not a List"
    assert len(dir_list) > 0, "Dir list given has no length"

    for i in range(len(dir_list)):
        try:
            abs_path = os.path.realpath(dir_list[i], strict=True)
            if os.path.isdir(abs_path):
                dir_list[i] = abs_path
            else:
                print(f"Directory path {dir_list[i]} does not go to a directory")
                return False

        except FileNotFoundError:
            print(f"Directory path {dir_list[i]} does not exist")
            return False

    return True

def validateFiles(file_list):
    assert isinstance(file_list, list), "File list is not a List"
    assert len(file_list) > 0, "File list given has no length"

    for i in range(len(file_list)):
        try:
            abs_path = os.path.realpath(file_list[i], strict=True)
            if os.path.isfile(abs_path):
                file_list[i] = abs_path
            else:
                print(f"File path {file_list[i]} does not go to a regular file")
                return False
        except FileNotFoundError:
            print(f"File path {file_list[i]} does not exist")
            return False

    return True


def traverseFiles(file_paths):
    assert isinstance(file_paths, list), "File list is not a List"
    assert len(file_paths) > 0, "File list given has no length"

    for path in file_paths:
        addMetadata(path)

def traverseDirs(dir_paths):
    assert isinstance(dir_paths, list), "Dir list is not a List"
    assert len(dir_paths) > 0, "File list given has no length"

    for path in dir_paths:
        try:
            for root, subdirs, files in os.walk(path):
                if files:
                    for file in files:
                        addMetadata(os.path.join(root, file))
        except OSError:
            error_log.append(f"Failed to walk through directory {path}")

def addMetadata(file_path):
    assert isinstance(file_path, str), "File path is not a string"
    assert file_path, "File name is empty or null"

    base_name, ext = os.path.splitext(file_path)
    if ext != ".mp3":
        return None

    base_name = os.path.basename(base_name)
    if not base_name:
        return None

    TEMP_DIR = "/tmp"

    #exiftool can't write to mp3 files as it can only read them not write
    command_args = ["ffmpeg", "-y", "-xerror", "-i", file_path]
    for meta_tag, meta_data in meta_dictionary.items():
        command_args.append("-metadata")
        command_args.append(f"{meta_tag}={meta_data}")

    temp_place = f"{TEMP_DIR}/{base_name}.mp3"
    command_args.append("-codec")
    command_args.append("copy")
    command_args.append(temp_place)

    proc_status = subprocess.call(command_args)
    if proc_status != 0:
        error_log.append(f"Failed to add metadata to {file_path}")
    else:
        move_args = ["mv", temp_place, file_path]
        proc_status = subprocess.call(move_args)
        if proc_status != 0:
            error_log.append(f"Failed to move {temp_place} to {file_path}")

if __name__ == "__main__":
    main()
