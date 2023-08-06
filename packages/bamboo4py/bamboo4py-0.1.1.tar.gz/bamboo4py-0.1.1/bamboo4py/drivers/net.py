from typing import Union
from netaddr import IPNetwork, IPAddress, IPSet
import ipaddress

AnyIPNetwork = Union[IPNetwork, ipaddress.IPv4Network, ipaddress.IPv6Network]
AnyIPv4Address = Union[IPAddress, ipaddress.IPv4Address]
AnyIPv6Address = Union[IPAddress, ipaddress.IPv6Address]
AnyIPAddress = Union[IPAddress, ipaddress.IPv4Address, ipaddress.IPv6Address]


def asipaddress(addr: AnyIPAddress) -> IPAddress:
    if isinstance(addr, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        return IPAddress(addr.exploded)
    else:
        return addr


def asipnetwork(subnet: AnyIPNetwork) -> IPNetwork:
    if isinstance(subnet, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
        return IPNetwork(subnet.exploded)
    else:
        return subnet


def pop_avaliable_ip_from_ipset(ipset: IPSet):
    result: IPAddress
    for addr in ipset:
        result = addr
        break
    ipset.remove(result)
    return result
