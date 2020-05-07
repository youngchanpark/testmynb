import re
from typing import List

from IPython.core.getipython import get_ipython



def remove_strings(text: str) -> str:
    """Removes strings
    
    Example
    -------
    >>> remove_strings('print("hello")')
    'print()'
    """
    return re.sub(r'(\'.*\')|(\".*\")', '', text)

def split_statements(text: str) -> List[str]:
    """Splits a string on `\n` and `;`.
    
    Examples
    --------
    >>> split_statements('print()\\nassert True')
    ['print()', 'assert True']
    >>> split_statements('print() ; assert True')
    ['print()', 'assert True']
    """
    # If you see closely in the first example in the docstring,
    # You'll notice that the newline is written as `\\n` rather than `\n`.
    # This is because `\n` is converted to a real newline when parsed as a docstring
    # and messes up doctest and reader-side of the docstring!
    split_text = re.split(r'\n|;', text) 
    return [line.strip() for line in split_text if line]

def assert_exists(split_text: List[str]) -> bool:
    """Checks whether an `assert` statement exists in the given `split_text` 
    Examples
    --------
    >>> assert_exists(['print()', 'assert True'])
    True
    >>> assert_exists(['print()'])
    False
    """
    assert_found = False
    for line in split_text:
        if re.match(r'^assert', line):
            assert_found = True
            break
    return assert_found

def search_assert(cell: str) -> bool:
    """
    >>> search_assert('print();assert True')
    True
    >>> search_assert('print()')
    False
    """
    stringless_cell: str = remove_strings(cell)
    split_text: List[str] = split_statements(stringless_cell)    
    assert_found: bool = assert_exists(split_text)

    return assert_found


def testcell(line, cell):
    interactive_shell = get_ipython()

    if ('-n' not in line) and (not search_assert(cell)):
        interactive_shell.run_code('print("[testmynb] Assert statement missing.")')
    interactive_shell.run_cell(cell)



def load_ipython_extension(ipython):
    ipython.register_magic_function(testcell, 'cell')



def intentional_error_func():
    undefiend_variable.undefined_method('this will error')