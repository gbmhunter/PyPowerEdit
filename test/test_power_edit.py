import os
import pytest
from typing import List

from power_edit import power_edit

@pytest.fixture
def init():
    
    return {
        'power_edit': power_edit.PowerEdit(),
        'script_path': os.path.dirname(os.path.realpath(__file__)) + os.sep
    }

def test_find_files_recursive_false(init):
    power_edit = init['power_edit']
    results = power_edit.find_files(os.path.join(init['script_path'], 'data', 'basic', '*.txt'), recursive=False)
    print(results)
    assert isinstance(results, List)
    truths = [ os.path.join('basic', 'test1.txt'), os.path.join('basic', 'test2.txt') ]
    print(truths)
    assert len(results) == len(truths)
    for result in results:
        match_found = False
        for truth in truths:
            if truth in result:
                match_found = True
        assert match_found

def test_find_files_recursive_true(init):
    power_edit = init['power_edit']
    results = power_edit.find_files(os.path.join(init['script_path'] ,'data', 'basic', '**/*.txt'), recursive=True)
    assert isinstance(results, List)
    truths = [ os.path.join('basic', 'test1.txt'), os.path.join('basic', 'test2.txt'), 
        os.path.join('basic', 'nested_dir', 'test3.txt') ]
    print(results)
    print(truths)
    assert len(results) == len(truths)
    for result in results:
        match_found = False
        for truth in truths:
            if truth in result:
                match_found = True
        assert match_found

def test_find_replace(init):
    power_edit = init['power_edit']
    results = power_edit.find_files(os.path.join(init['script_path'], 'data', 'basic', 'test1.txt'))
    assert len(results) == 1
    result = power_edit.find_replace(results[0], 'hello', 'bonjour')
    assert result == "bonjour\ngoodbye\nbonjour\ngoodbye"

def test_find_replace_regex_simple(init):
    power_edit = init['power_edit']

    def replace_fn(find_str):
        print(f'replace_fn() called. find_str = {find_str}')
        return 'replace'

    results = power_edit.find_files(os.path.join(init['script_path'], 'data', 'regex', 'multiline.txt'))
    assert len(results) == 1
    result = power_edit.find_replace(results[0], 'se.*d', replace_fn, regex=True)
    assert result == "first\nreplace\nthird\nfourth\nfifth"

def test_find_replace_regex_multiline(init):
    power_edit = init['power_edit']

    def replace_fn(find_str):
        print(f'replace_fn() called. find_str = {find_str}')
        return 'replace'

    results = power_edit.find_files(os.path.join(init['script_path'], 'data', 'regex', 'multiline.txt'))
    assert len(results) == 1
    result = power_edit.find_replace(results[0], 'sec.*ourth', replace_fn, regex=True, multiline=True)
    assert result == "first\nreplace\nfifth"