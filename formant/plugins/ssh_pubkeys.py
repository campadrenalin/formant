from pathlib import Path

root_path = Path.home() / '.ssh'

def get_key(kind='rsa'):
    assert kind in ('rsa', 'dsa')
    path = root_path / f'id_{kind}.pub'
    try:
        with open(path, 'r') as f:
            return f.read()
    except:
        return None

rsa_key = get_key('rsa')
dsa_key = get_key('dsa')
any_key = rsa_key or dsa_key
