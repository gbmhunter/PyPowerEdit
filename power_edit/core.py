#!/usr/bin/env python3

import fileinput
import os
import re

# Set this to True to perform a simulation run, which will not modify anything, and will
# print more info about changes to stdout
SIM_RUN = True

def find_files(extension: str):
    matched_files = list()
    for root, dirs, files in os.walk('.'):
        print(files)
        for file in files:
            if file.endswith(extension):
                matched_files.append(os.path.join(root, file))

    if SIM_RUN:
        print(f'matched_files = {matched_files}')

    return matched_files

def find_replace(file_path, find_str, replace_str):
    print(f'file_path = {file_path}, find_str = {find_str}')

    # Read in the file
    with open(file_path, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(find_str, replace_str)

    if SIM_RUN:
        print(f'filedata = {filedata}')

    # Write the file out again
    if not SIM_RUN:
        with open(file_path, 'w') as file:
            file.write(filedata)

def find_insert(file_path: str, find_str: str, insert_str: str) -> None:
    """

    Use '\n' to match new lines.

    Iterataively tries to find and insert matches through the file. Could get stuck in recursive loop if insert string
    contains find string.

    Args:
        file_path (str): The file to operate on.
        find_str (str): The string to find in the file. Does not support regex.
        insert_str (str): The string to insert after the last character in find_str.

    Returns:
        None
    """
    with open(file_path, 'r') as file :
        filedata = file.read()


    start_index = None
    while True:
        start_index = filedata.find(find_str, start_index)
        if start_index == -1:
            break

        insert_at = start_index + len(find_str)
        # print(insert_at)
        filedata = filedata[:insert_at] + insert_str + filedata[insert_at:]

        # Start looking for next match one char past where last
        # match was found
        start_index += 1

    if SIM_RUN:
        print(f'find_insert() finished. filedata = {filedata}')
    else:
        with open(file_path, 'w') as file:
            file.write(filedata)


def main():
    files = find_files('.txt')

    for file in files:
        # find_replace(file, 'hello', 'bonjour')
        find_insert(file, 'insert\n', 'test\n')

if __name__ == '__main__':
    main()


