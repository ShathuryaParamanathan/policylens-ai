import ipaddress
import socket
from urllib.parse import urlparse


ALLOWED_SCHEMES = {
    "http",
    "https",
}


def is_public_ip(ip_address: str) -> bool:
    """
    Return True only for publicly routable IP addresses.

    Blocks:
    - private IPs
    - loopback
    - link-local
    - multicast
    - reserved
    - unspecified
    """

    try:
        ip = ipaddress.ip_address(
            ip_address
        )

        return not (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        )

    except ValueError:
        return False


def resolve_hostname(hostname: str) -> list[str]:
    """
    Resolve hostname to IPv4/IPv6 addresses.
    """

    try:
        results = socket.getaddrinfo(
            hostname,
            None,
            type=socket.SOCK_STREAM,
        )

    except socket.gaierror as error:
        raise ValueError(
            f"Unable to resolve hostname: {hostname}"
        ) from error

    addresses = set()

    for result in results:

        address = result[4][0]

        addresses.add(address)

    return list(addresses)


def validate_url(url: str) -> str:
    """
    Validate a user-provided URL before crawling.

    Returns the normalized URL when valid.

    Raises ValueError for unsafe URLs.
    """

    if not url:
        raise ValueError(
            "URL is required."
        )

    parsed = urlparse(url)

    # -----------------------------------------
    # Scheme validation
    # -----------------------------------------

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        raise ValueError(
            "Only HTTP and HTTPS URLs are allowed."
        )

    # -----------------------------------------
    # Host validation
    # -----------------------------------------

    hostname = parsed.hostname

    if not hostname:
        raise ValueError(
            "URL must contain a hostname."
        )

    hostname = hostname.lower().rstrip(".")

    # -----------------------------------------
    # Block embedded credentials
    # -----------------------------------------

    if parsed.username or parsed.password:
        raise ValueError(
            "URLs containing username or password "
            "credentials are not allowed."
        )

    # -----------------------------------------
    # Block localhost names
    # -----------------------------------------

    blocked_hostnames = {
        "localhost",
        "localhost.localdomain",
        "ip6-localhost",
        "ip6-loopback",
    }

    if hostname in blocked_hostnames:
        raise ValueError(
            "Localhost URLs are not allowed."
        )

    # -----------------------------------------
    # Direct IP validation
    # -----------------------------------------

    try:
        ip = ipaddress.ip_address(
            hostname
        )

        if not is_public_ip(
            str(ip)
        ):
            raise ValueError(
                "Private or reserved IP addresses "
                "are not allowed."
            )

    except ValueError as error:

        # If hostname is not an IP address,
        # resolve it below.
        try:
            ipaddress.ip_address(
                hostname
            )

            raise error

        except ValueError:
            pass

    # -----------------------------------------
    # DNS resolution
    # -----------------------------------------

    addresses = resolve_hostname(
        hostname
    )

    if not addresses:
        raise ValueError(
            "Hostname did not resolve to an IP address."
        )

    for address in addresses:

        if not is_public_ip(address):
            raise ValueError(
                "Hostname resolves to a private, "
                "local, or reserved IP address."
            )

    # -----------------------------------------
    # Normalize URL
    # -----------------------------------------

    normalized_url = (
        f"{parsed.scheme.lower()}://"
        f"{hostname}"
    )

    if parsed.port:
        normalized_url += (
            f":{parsed.port}"
        )

    if parsed.path:
        normalized_url += parsed.path

    if parsed.query:
        normalized_url += (
            f"?{parsed.query}"
        )

    return normalized_url
