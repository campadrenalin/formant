import dns.resolver as dr

def get_ip_text(*args, resolver=dr):
    return resolver.query(*args)[0].to_text().strip('"')

# Google nameserver useful for deriving public IP
ns1 = dr.Resolver(configure=False)
ns1.nameservers = [get_ip_text('ns1.google.com')]

def get_ipv4():
    return get_ip_text('o-o.myaddr.l.google.com', 'TXT', resolver=ns1)

ipv4 = get_ipv4()

if __name__ == '__main__':
    print(ipv4)
