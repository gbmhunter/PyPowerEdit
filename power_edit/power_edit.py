#!/usr/bin/env python3

import fileinput
import glob
import os
import re
from typing import Callable, List, Optional, Union

class PowerEdit:

    def __init__(self):
        # Set this to True to perform a simulation run, which will not modify anything, and will
        # print more info about changes to stdout
        self.sim_run: bool = True

    def find_files(self, pathname, recursive=False):
        return glob.glob(pathname, recursive=recursive)

    def find_replace(self, file_path: str, find_str: str, replace: Union[str, Callable], 
        regex: bool=False,
        multiline: bool=False):
        """
        Replaces all occurance of `find_str` with `replace_str` in the file specified by `file_path`.
        """

        # Read in the file
        with open(file_path, 'r') as file :
            filedata = file.read()

        if multiline:
            regex_flags = re.MULTILINE|re.DOTALL
        else:
            regex_flags = 0

        # Replace the target string
        if not regex:
            filedata = filedata.replace(find_str, replace)
        elif isinstance(replace, str):
            regex = re.compile(find_str, regex_flags)
            filedata = re.sub(regex, replace, filedata)
        elif callable(replace):
            regex = re.compile(find_str, regex_flags)

            while(True):
                match = regex.search(filedata)

                # Exit out of find/replace loop if we don't find anymore matches
                if match is None:
                    break

                group = match.group()
                replacement_text = replace(group)
                filedata = filedata[:match.start()] + replacement_text + filedata[match.end():]

        if self.sim_run:
            print(f'find_replace() ifnished. replaced filedata = {filedata}')

        # Write the file out again
        if not self.sim_run:
            with open(file_path, 'w') as file:
                file.write(filedata)

        return filedata

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
