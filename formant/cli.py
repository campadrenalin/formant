import sys, os
import logging
from formant import template, plugins, logger

def parse(argv):
    positional = []
    flag_args  = {}
    current_flag = None

    for arg in argv:
        if current_flag:
            flag_args[current_flag] = arg
            current_flag = None
            continue

        if arg.startswith('--'):
            arg, eq, value = arg.partition('=')
            current_flag = arg.strip('-').replace('-', '_')
            if eq:
                flag_args[current_flag] = value
                current_flag = None
            continue

        if arg == '-v':
            logger.setLevel(logging.DEBUG)
            continue

        positional.append(arg)

    assert current_flag is None, f'No value provided for {current_flag}'
    return positional, flag_args

def read_file(filename='-'):
    if filename == '-':
        return sys.stdin.read()
    with open(filename, 'r') as f:
        return f.read()

def fmnt_print(*argv, **env):
    '''
    formant print [filename] --some-arg='Some value'
    '''
    positional, flag_args = parse(argv)
    assert len(positional) <= 1, "Expect one positional argument (filename)"

    text = read_file(*positional)
    try:
        print(template(text, flag_args, plugins.registry, env))
    except NameError as ne:
        import re
        name = re.fullmatch(r"name '(\w+)' is not defined", str(ne))
        if name:
            ne = name.group(1)
        print(f'Missing parameter: {ne}', file=sys.stderr)

def fmnt_help(subcommand):
    '''
    formant help [subcommand] :: This message
    formant print             :: Print a template with parameter substitution
    '''
    print(subcommand.__doc__, file=sys.stderr)

def run_cli(argv=sys.argv, env=os.environ):
    subcommands = {
        'print': fmnt_print,
        'help':  fmnt_help,
    }
    def get_handler(argn):
        if len(argv)-1 < argn:
            return fmnt_help
        return subcommands.get(argv[argn], fmnt_help)

    handler = get_handler(1)
    if handler is fmnt_help:
        return fmnt_help(get_handler(2))
    else:
        return handler(*argv[2:], **env)

if __name__ == '__main__':
    run_cli()
