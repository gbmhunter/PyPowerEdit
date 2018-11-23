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

    def find_files(self, pathname: str, recursive: bool=False) -> List[str]:
        return glob.glob(pathname, recursive=recursive)

    def find_replace(self, file_path: str, find_str: str, replace_str: str) -> str:
        """
        Basic find/replace function that does not use regex. Will write changes to the file
        if `self.sim_run=True`.

        Args:
            file_path: Absolute path to the file you wish to perform find/replace on.
            find_str: The string you wish to search for (not regex).
            replace_str: The string you wish the found text to be replaced with.
        Returns:
            The data that is written to the file after all find/replace operations have occurred.
        """

        # Read in the file
        with open(file_path, 'r') as file :
            filedata = file.read()

        filedata = filedata.replace(find_str, replace_str)

        if self.sim_run:
            print(f'find_replace() finished. replaced filedata = {filedata}')

        # Write the file out again
        if not self.sim_run:
            with open(file_path, 'w') as file:
                file.write(filedata)

        return filedata

    def find_replace_regex(
        self, file_path: str, regex_str: str, replace: Union[str, Callable], multiline: bool=False) -> str:
        """
        Advanced find/replace function that uses regex to find matching text.

        Args:
            file_path: Absolute path to the file you wish to perform find/replace on.
            regex_str: The regex pattern (as a string) that you want to match against.
            replace: If replace is a string, the matched pattern will be replaced directly with this
                string. If replace is a function, the function will be called, passing in the 
                found text as the first and only parameter. The found text will be replaced with 
                whatever the function returns.
            multiline: If True, matching will be performed with the re.MULTILINE and re.DOTALL flags
                enabled.
        Returns:
            The data that is written to the file after all find/replace operations have occurred.
        """

        # Read in the file
        with open(file_path, 'r') as file :
            filedata = file.read()

        if multiline:
            regex_flags = re.MULTILINE|re.DOTALL
        else:
            regex_flags = 0

        # Replace the target string
        if isinstance(replace, str):
            regex = re.compile(regex_str, regex_flags)
            filedata = re.sub(regex, replace, filedata)
        elif callable(replace):
            regex = re.compile(regex_str, regex_flags)

            while(True):
                match = regex.search(filedata)

                # Exit out of find/replace loop if we don't find anymore matches
                if match is None:
                    break

                group = match.group()
                replacement_text = replace(group)
                if not isinstance(replacement_text, str):
                    raise ValueError('Returned object from replace function must be a string.')
                filedata = filedata[:match.start()] + replacement_text + filedata[match.end():]
        else:
            raise RuntimeError(f'replace must be either a string or a callable object. replace = {replace}.')

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

        