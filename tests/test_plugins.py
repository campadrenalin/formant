import formant.plugins as plugs
import re

def test_find_packages():
    pkgs = set(plugs.find_packages())
    assert ('public_ip', 'formant.plugins.public_ip') in pkgs

def test_ipv4():
    ipv4 = plugs.registry.public_ip.ipv4
    assert re.fullmatch(
        r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',
        ipv4)

def test_pubkeys():
    key = plugs.registry.ssh_pubkeys.any_key
    assert key
    assert re.match('ssh-(rsa|dsa) ', key)
