import formant.plugins as plugs
import re

def test_find_packages():
    pkgs = set(plugs.find_packages())
    assert ('public_ip', 'formant.plugins.public_ip') in pkgs

re_ipv4 = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')

def test_registry_method():
    ipv4 = plugs.registry.public_ip.ipv4()
    assert re_ipv4.fullmatch(ipv4)

def test_registry_format():
    ipv4 = format(plugs.registry.public_ip.ipv4)
    assert re_ipv4.fullmatch(ipv4)
