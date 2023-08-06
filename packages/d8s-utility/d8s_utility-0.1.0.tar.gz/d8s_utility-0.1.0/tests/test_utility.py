import os

import pytest

from d8s_utility import (
    copy_first_arg,
    first_unsorted_value,
    is_sorted,
    last_unsorted_value,
    map_first_arg,
    prettify,
    repeat_concurrently,
    request_or_read,
    request_or_read_first_arg,
    retry_if_no_result,
    sorted_values,
    stringify_first_arg,
    subprocess_run,
    unique_items,
    unsorted_values,
    wait_and_retry_on_failure,
    zip_if_same_length,
)

TEST_DIRECTORY_PATH = './test_files'
NON_EXISTENT_FILE_PATH = './foo'
TEST_FILE_NAME = 'a'
EXISTING_FILE_PATH = os.path.join(TEST_DIRECTORY_PATH, TEST_FILE_NAME)


def test_zip_if_same_length_1():
    result = tuple(zip_if_same_length([1, 2], [1, 2]))
    assert result == ((1, 1), (2, 2))

    with pytest.raises(ValueError):
        tuple(zip_if_same_length([1, 2], [1, 2, 3]))


def test_unique_items_1():
    result = unique_items([1, 2, 3], [2, 3, 4])
    assert result == {'a': {1}, 'b': {4}}

    # TODO: as of September 2020, this is failing... not sure if we should add a work around or not
    # result = unique_items([{'a': 1}, {'b': 2}], [{'a': 1}, {'c': 2}])
    # assert result == {'a': [{'b': 1}], 'b': [{'c': 1}]}


def test_unsorted_values_1():
    l = [1, 2, 4, 3]
    results = list(unsorted_values(l))
    assert results == [4, 3]

    l = [1, 3, 2, 4]
    results = list(unsorted_values(l, descending=True))
    assert results == [1, 4]

    l = [1, 2, 1, 3]
    results = list(unsorted_values(l))
    assert results == [2, 1]


def test_sorted_values_1():
    l = [1, 2, 4, 3]
    results = list(sorted_values(l))
    assert results == [1, 2]

    l = [1, 3, 2, 4]
    results = list(sorted_values(l, descending=True))
    assert results == [3, 2]

    l = [1, 2, 1, 3]
    results = list(sorted_values(l))
    assert results == [1, 3]


def test_last_unsorted_value_1():
    l = [1, 2, 3, 4]
    assert last_unsorted_value(l) is None
    assert last_unsorted_value(l, descending=True) == 4

    l = [4, 3, 2, 1]
    assert last_unsorted_value(l) == 1
    assert last_unsorted_value(l, descending=True) is None

    l = 'abc'
    assert last_unsorted_value(l) is None
    assert last_unsorted_value(l, descending=True) == 'c'

    l = 'cdf'
    assert last_unsorted_value(l) is None
    assert last_unsorted_value(l, descending=True) == 'f'

    l = 'cba'
    assert last_unsorted_value(l) == 'a'
    assert last_unsorted_value(l, descending=True) is None


def test_first_unsorted_value_1():
    l = [1, 2, 3, 4]
    assert first_unsorted_value(l) is None
    assert first_unsorted_value(l, descending=True) == 1

    l = [4, 3, 2, 1]
    assert first_unsorted_value(l) == 4
    assert first_unsorted_value(l, descending=True) is None

    l = 'abc'
    assert first_unsorted_value(l) is None
    assert first_unsorted_value(l, descending=True) == 'a'

    l = 'cdf'
    assert first_unsorted_value(l) is None
    assert first_unsorted_value(l, descending=True) == 'c'

    l = 'cba'
    assert first_unsorted_value(l) == 'c'
    assert first_unsorted_value(l, descending=True) is None


@pytest.mark.network
def test_request_or_read_1():
    s = os.path.abspath(__file__)
    result = request_or_read(s)
    print(result)
    assert 'def test_request_or_read_1():' in result

    s = 'https://hightower.space/projects'
    result = request_or_read(s)
    assert 'Floyd Hightower' in result


def test_is_sorted_1():
    l = [1, 2, 3, 4]
    assert is_sorted(l)

    l = [4, 3, 2, 1]
    assert not is_sorted(l)
    assert is_sorted(l, descending=True)

    l = 'abc'
    assert is_sorted(l)

    l = 'cdf'
    assert is_sorted(l)

    l = 'cba'
    assert not is_sorted(l)


def test_prettify_1():
    d = {'nums': [i for i in range(0, 10)], 'ids': 'a' * 64}
    result = prettify(d)
    assert (
        result
        == '''{'ids': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
 'nums': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}'''
    )


def test_subprocess_run_docs_1():
    command = 'ls'
    stdout, stderr = subprocess_run(command)
    assert 'LICENSE\n' in stdout
    assert 'README.md\n' in stdout

    command = 'ls -la'
    stdout, stderr = subprocess_run(command)
    assert 'total ' in stdout
    assert 'drwxr-xr-x' in stdout

    command = ['ls', '-la']
    stdout, stderr = subprocess_run(command)
    assert 'total ' in stdout
    assert 'drwxr-xr-x' in stdout


def test_subprocess_run_errors_1():
    command = 'a'
    # TODO: not sure why this raises a FileNotFoundError rather than an error saying that the given command was not found
    with pytest.raises(FileNotFoundError):
        subprocess_run(command)


def test_subprocess_run_input():
    # this test was inspired by the comment here: https://gist.github.com/waylan/2353749#gistcomment-2843563
    test_input = 'c\nb\na'
    stdout, stderr = subprocess_run('sort', input_=test_input)
    assert stdout == 'a\nb\nc\n'


@stringify_first_arg
def stringify_first_arg_test_func(arg):
    return arg


def test_stringify_first_arg_1():
    result = stringify_first_arg_test_func('foo')
    assert result == 'foo'

    result = stringify_first_arg_test_func(1)
    assert result == '1'


@retry_if_no_result(wait_seconds=3)
def retry_if_no_result_test_func():
    return None


def test_retry_if_no_result_1():
    from democritus_timer import timer_start, timer_stop

    # time the execution
    timer_name = timer_start()
    result = retry_if_no_result_test_func()
    execution_time = timer_stop(timer_name)

    # make sure the retry_if_no_result_test_func was run twice with the appropriate amount of time in between
    assert execution_time > 3
    assert result is None


@copy_first_arg
def copy_first_arg_test_func_a(a):
    return a


@pytest.mark.network
def test_copy_first_arg_1():
    from democritus_html import html_soupify
    from democritus_networking import get

    # a RecursionError will occur when trying to do a deep copy of beautifulsoup objects - see: https://github.com/biopython/biopython/issues/787, https://bugs.python.org/issue5508, and https://github.com/cloudtools/troposphere/issues/648...
    # this test makes sure that the `copy_first_arg` decorator will properly fall back from a deep copy to a shallow copy
    html_text = get('https://hightower.space/', process_response=True)
    soup = html_soupify(html_text)
    copy_first_arg_test_func_a(soup)


@map_first_arg
def map_first_arg_test_func_1(a):
    return a[::-1]


def test_map_first_arg_1():
    result = map_first_arg_test_func_1('abc')
    assert result == 'cba'

    result = map_first_arg_test_func_1(['abc', 'cat'])
    assert result == ['cba', 'tac']


@map_first_arg
def map_first_arg_test_func_kwargs(a, reverse=True):
    if reverse:
        return a[::-1]
    else:
        return a


def test_map_first_arg_kwargs():
    result = map_first_arg_test_func_kwargs('abc', reverse=True)
    assert result == 'cba'

    with pytest.raises(TypeError):
        result = map_first_arg_test_func_kwargs('abc', 'def', 'ghi')

    result = map_first_arg_test_func_kwargs('abc', reverse=False)
    assert result == 'abc'

    result = map_first_arg_test_func_kwargs(['abc', 'cat'], reverse=True)
    assert result == ['cba', 'tac']

    result = map_first_arg_test_func_kwargs(['abc', 'cat'], reverse=False)
    assert result == ['abc', 'cat']


@map_first_arg
def map_first_arg_test_func_multiple_args(a, b, reverse=True):
    if reverse:
        return a[::-1], b
    else:
        return a, b


def test_map_first_arg_multiple_args():
    result = map_first_arg_test_func_multiple_args('abc', 'a', reverse=True)
    assert result == ('cba', 'a')

    result = map_first_arg_test_func_multiple_args('abc', ['foo'], reverse=False)
    assert result == ('abc', ['foo'])

    result = map_first_arg_test_func_multiple_args(['abc', 'cat'], '', reverse=True)
    assert result == [('cba', ''), ('tac', '')]

    result = map_first_arg_test_func_multiple_args(['abc', 'cat'], None, reverse=False)
    assert result == [('abc', None), ('cat', None)]


@repeat_concurrently()
def repeat_concurrently_test_func_a():
    return 1


@repeat_concurrently(n=100)
def repeat_concurrently_test_func_b():
    return 1


def test_repeat_concurrently_1():
    results = repeat_concurrently_test_func_a()
    assert tuple(results) == (1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

    results = tuple(repeat_concurrently_test_func_b())
    assert len(results) == 100
    assert results.count(1) == 100


@wait_and_retry_on_failure(wait_seconds=3)
def wait_and_retry_on_failure_test_func():
    assert 1 == 2


def test_wait_and_retry_on_failure_1():
    from democritus_timer import timer_start, timer_stop

    # time the execution
    timer_name = timer_start()
    # catch the error (which will occur both the first and second times the app is run, but will not be caught by the decorator the second time)
    with pytest.raises(AssertionError):
        wait_and_retry_on_failure_test_func()
    execution_time = timer_stop(timer_name)

    # make sure the wait_and_retry_on_failure_test_func was run twice with the appropriate amount of time in between
    assert execution_time > 3


@request_or_read_first_arg
def request_or_read_first_arg_test_func(a):
    return a


def test_request_or_read_first_arg_1():
    # test a url
    s = 'https://hightower.space/projects'
    result = request_or_read_first_arg_test_func(s)
    assert 'Floyd Hightower' in result

    # test a file path
    s = os.path.abspath(__file__)
    result = request_or_read_first_arg_test_func(s)
    assert 'def test_request_or_read_first_arg_1():' in result

    # test a non-existent file path
    s = '/foo/bar/non-existent.txt'
    result = request_or_read_first_arg_test_func(s)
    assert result == s

    # test another string
    s = 'foobar'
    result = request_or_read_first_arg_test_func(s)
    assert result == s
