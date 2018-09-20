#!/usr/bin/env python3

import fileinput
import glob
import os
import re
from typing import List, Optional

class PowerEdit:

    def __init__(self):
        # Set this to True to perform a simulation run, which will not modify anything, and will
        # print more info about changes to stdout
        self.sim_run: bool = True

    # def find_files(self, base_dir: str, extension: Optional[str]=None) -> List:
    #     """
    #     Finds file matching specfic patterns.

    #     Args:
    #         base_dir (str): An absolute path to the base directory to begin searching to files from.
    #     """

    #     matched_files = list()
    #     for root, dirs, files in os.walk(base_dir):
    #         print(files)
    #         for file in files:
    #             if file.endswith(extension):
    #                 matched_files.append(os.path.join(root, file))

    #     if self.sim_run:
    #         print(f'matched_files = {matched_files}')

    #     return matched_files

    def find_files(self, pathname, recursive=False):
        return glob.glob(pathname, recursive=recursive)

    def find_replace(self, file_path, find_str, replace_str):
        print(f'file_path = {file_path}, find_str = {find_str}')

        # Read in the file
        with open(file_path, 'r') as file :
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(find_str, replace_str)

        if self.sim_run:
            print(f'filedata = {filedata}')

        # Write the file out again
        if not self.sim_run:
            with open(file_path, 'w') as file:
                file.write(filedata)

    def find_insert(self, file_path: str, find_str: str, insert_str: str) -> None:
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

        if self.sim_run:
            print(f'find_insert() finished. filedata = {filedata}')
        else:
            with open(file_path, 'w') as file:
                file.write(filedata)
