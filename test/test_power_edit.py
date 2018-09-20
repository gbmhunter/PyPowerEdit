import os
import pytest
from typing import List

from power_edit import power_edit

@pytest.fixture
def init():
    
    return {
        'power_edit': power_edit.PowerEdit(),
        'script_path': os.path.dirname(os.path.realpath(__file__)) + '/'
    }

# def test_temp(init):
#     power_edit = init['power_edit']
#     results = power_edit.find_files(init['script_path'], 'txt')
#     assert isinstance(results, List)
#     assert len(results) == 1
#     assert 'data/' in results[0]

def test_find_files_recursive_false(init):
    power_edit = init['power_edit']
    results = power_edit.find_files(init['script_path'] + '**/*.txt', recursive=False)
    assert isinstance(results, List)
    truths = [ 'data/test1.txt', 'data/test2.txt' ]
    assert len(results) == len(truths)
    for result in results:
        match_found = False
        for truth in truths:
            if truth in result:
                match_found = True
        assert match_found

def test_find_files_recursive_true(init):
    power_edit = init['power_edit']
    results = power_edit.find_files(init['script_path'] + '**/*.txt', recursive=True)
    assert isinstance(results, List)
    truths = [ 'data/test1.txt', 'data/test2.txt', 'data/nested_dir/test3.txt' ]
    assert len(results) == len(truths)
    for result in results:
        match_found = False
        for truth in truths:
            if truth in result:
                match_found = True
        assert match_found

def test_find_replace(init):
    power_edit = init['power_edit']
    results = power_edit.find_files(init['script_path'] + 'data/test1.txt')
    assert len(results) == 1
    result = power_edit.find_replace(results[0], 'hello', 'bonjour')
    assert result == "bonjour\ngoodbye\nbonjour\ngoodbye"