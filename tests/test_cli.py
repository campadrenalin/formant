import pytest
from unittest.mock import patch
from formant.cli import *
from formant.plugins.public_ip import ipv4

@pytest.mark.parametrize('argv, pos, flags', [
    ([], [], {}),
    (['A positional arg'], ['A positional arg'], {}),
    (['one', 'two', 'three'], ['one', 'two', 'three'], {}),
    (['--flag', 'value'], [], {'flag': 'value'}),
    (['--flag-with-hyphens', 'value'], [], {'flag_with_hyphens': 'value'}),
    (['--flag=Some Text'], [], {'flag': 'Some Text'}),
    (['--flag=Some=Text'], [], {'flag': 'Some=Text'}),
    (['pos1', '--flag1=f1', 'pos2', '--flag2', 'f2'],
        ['pos1', 'pos2'],
        {'flag1':'f1', 'flag2':'f2'}),
])
def test_parse(argv, pos, flags):
    assert parse(argv) == (pos, flags)

files = {
    '-': 'A simple STDIN example',
    'hello.txt': 'Hello, <% USER %>!',
    'ip_addr.txt': 'Your public IPv4 address is <% public_ip.ipv4 %>.',
}
def fake_read_file(filename='-'):
    return files[filename]

@pytest.mark.parametrize('argv, env, expected', [
    ([], {},
        ('A simple STDIN example\n', '') ),

    (['hello.txt', '--USER=Alice'], {},
        ('Hello, Alice!\n', '') ),
    (['hello.txt'], {'USER': 'Bob'},
        ('Hello, Bob!\n', '') ),
    (['hello.txt'], {},
        ('', 'Missing parameter: USER\n') ),

    (['ip_addr.txt'], {},
        (f'Your public IPv4 address is {ipv4}.\n', '') ),
])
@patch('formant.cli.read_file', fake_read_file)
def test_fmnt_print(argv, env, expected, capsys):
    fmnt_print(*argv, **env)
    assert capsys.readouterr() == expected
