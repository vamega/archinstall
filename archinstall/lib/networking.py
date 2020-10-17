import fcntl
import socket
import struct

# Linux Socket IO Config Interface Constant to get Hardware Address
SIOCGIFHWADDR = 0x8927


def get_hw_addr(ifname: str) -> str:
    """
    Get the MAC address for the a given interface

    :param ifname: The name of the interface.
    :return: The MAC address separated as a string in the format xx-xx-xx-xx-xx-xx
    :raises: OSError If a MAC address cannot be determined for the interface.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(
        s.fileno(), SIOCGIFHWADDR, struct.pack("256s", bytes(ifname, "utf-8")[:15])
    )
    return ":".join("%02x" % b for b in info[18:24])


def list_interfaces(skip_loopback=True) -> dict[str, str]:
    """
    Get a list of network interfaces by their mac addresses.

    :param skip_loopback: True if the loopback interface should be present in
        the returned mapping
    :return: A dictionary network addresses keyed by the mac address of the interface.
    """
    interfaces = {}
    for index, iface in socket.if_nameindex():
        if skip_loopback and iface == "lo":
            continue

        mac = get_hw_addr(iface).replace(":", "-")
        interfaces[mac] = iface
    return interfaces
